import hashlib
import requests
import PySimpleGUI as sg
from db import initialize_db
from crypto_utils import create_master_key
from entries import get_all_entries, add_entry, update_entry, delete_entry, generate_password
from gui import \
    entry_window  # entry_window() muss so angepasst sein, dass es ein Passwortfeld (key "password") und einen Textindikator (key "pwd_strength") enthält.


def check_password_strength(password):
    """
    Prüft, ob das Passwort in der HaveIBeenPwned-Datenbank vorkommt.
    Gibt (True, 0) zurück, wenn das Passwort nicht gefunden wurde (stark),
    andernfalls (False, count), wobei count angibt, wie oft das Passwort gefunden wurde.
    """
    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError("Fehler beim Abrufen der Daten von der API.")

    for line in response.text.splitlines():
        h, count = line.split(':')
        if h == suffix:
            return False, int(count)
    return True, 0


def main():
    initialize_db()
    sg.theme("SystemDefault")

    # --- Login-Bereich ---
    login_column = [
        [sg.Text("Bitte Master-Passwort eingeben:", font=("Segoe UI", 12))],
        [sg.Input(password_char="*", key="master", font=("Segoe UI", 12))],
        [sg.Text("", key="error", size=(40, 1), text_color="red", font=("Segoe UI", 10))],
        [sg.Button("Login", key="login_btn", font=("Segoe UI", 12))]
    ]

    # --- Hauptbereich mit Symbol-Buttons neben der Tabelle ---
    main_column = [
        [sg.Table(values=[], headings=["ID", "Website", "Username", "Passwort", "Notizen"],
                  key="-TABLE-", auto_size_columns=True, display_row_numbers=False,
                  num_rows=10, enable_events=True, font=("Segoe UI", 10))],
        [sg.Button("➕", key="new", tooltip="Neuer Eintrag", font=("Segoe UI", 12), border_width=0, pad=(5, 5)),
         sg.Button("✏️", key="edit", tooltip="Bearbeiten", font=("Segoe UI", 12), border_width=0, pad=(5, 5)),
         sg.Button("🗑️", key="delete", tooltip="Löschen", font=("Segoe UI", 12), border_width=0, pad=(5, 5)),
         sg.Button("🔄", key="refresh", tooltip="Aktualisieren", font=("Segoe UI", 12), border_width=0, pad=(5, 5)),
         sg.Button("🔑", key="gen_pw", tooltip="Passwort generieren", font=("Segoe UI", 12), border_width=0, pad=(5, 5)),
         sg.Button("Beenden", key="exit", font=("Segoe UI", 12))]
    ]

    # --- Gesamtlayout: Login-Bereich sichtbar, Hauptbereich zunächst ausgeblendet ---
    layout = [[
        sg.Column(login_column, key="login_col", element_justification="center"),
        sg.Column(main_column, key="main_col", visible=False)
    ]]

    window = sg.Window("Password Manager - GitHub Style", layout, finalize=True, resizable=True)
    window.bind("<Return>", "login_enter")
    table_elem = window["-TABLE-"]
    table_elem.Widget.bind("<Double-Button-1>", lambda event: window.write_event_value('-TABLE-DOUBLE-', event))

    # Fensterzentrierung anhand fester Maße (500x350)
    root = window.TKroot
    root.update_idletasks()
    window_width = 500
    window_height = 350
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_position = (screen_width // 2) - (window_width // 2)
    y_position = (screen_height // 2) - (window_height // 2)
    window.move(x_position, y_position)

    fernet_obj = None

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "exit"):
            break

        # --- Login-Phase ---
        if window["login_col"].visible:
            if event in ("login_btn", "login_enter"):
                master = values["master"]
                fernet_obj = create_master_key(master)
                if fernet_obj is not None:
                    window["login_col"].update(visible=False)
                    window["main_col"].update(visible=True)
                    entries = get_all_entries(fernet_obj)
                    table_values = [[e['id'], e['website'], e['username'], e['password'], e['notes']] for e in entries]
                    window["-TABLE-"].update(values=table_values)
                else:
                    window["error"].update("Falsches Master-Passwort!")
            continue

        # --- Hauptbereich ---
        if event == "refresh":
            entries = get_all_entries(fernet_obj)
            table_values = [[e['id'], e['website'], e['username'], e['password'], e['notes']] for e in entries]
            window["-TABLE-"].update(values=table_values)
        elif event == "new":
            entry_win = entry_window()
            while True:
                e_event, e_values = entry_win.read()
                if e_event in (sg.WINDOW_CLOSED, "Abbrechen"):
                    break
                # Echtzeit-Überprüfung im neuen Eintragsfenster:
                if e_event == "password":
                    pwd = e_values["password"]
                    try:
                        is_strong, breaches = check_password_strength(pwd)
                    except Exception as ex:
                        entry_win["pwd_strength"].update("Fehler bei API")
                        continue
                    if breaches > 0:
                        strength_text = f"Schwach ({breaches} gefunden)"
                        strength_color = "red"
                    else:
                        if len(pwd) < 8:
                            strength_text = "Schwach"
                            strength_color = "red"
                        elif len(pwd) < 12:
                            strength_text = "Normal"
                            strength_color = "yellow"
                        else:
                            strength_text = "Gut"
                            strength_color = "green"
                    entry_win["pwd_strength"].update(value=strength_text, text_color=strength_color)

                if e_event == "-GEN-":
                    gen_pw = generate_password()
                    entry_win["password"].update(gen_pw)
                    try:
                        is_strong, breaches = check_password_strength(gen_pw)
                    except Exception as ex:
                        entry_win["pwd_strength"].update("Fehler bei API")
                    else:
                        if breaches > 0:
                            strength_text = f"Schwach ({breaches} gefunden)"
                            strength_color = "red"
                        else:
                            if len(gen_pw) < 8:
                                strength_text = "Schwach"
                                strength_color = "red"
                            elif len(gen_pw) < 12:
                                strength_text = "Normal"
                                strength_color = "yellow"
                            else:
                                strength_text = "Gut"
                                strength_color = "green"
                        entry_win["pwd_strength"].update(value=strength_text, text_color=strength_color)

                if e_event == "Speichern":
                    pwd = e_values['password']
                    is_strong, breaches = check_password_strength(pwd)
                    if breaches > 0:
                        answer = sg.popup_yes_no(
                            f"Das Passwort wurde {breaches} mal gefunden und gilt als schwach.\nMöchtest du es trotzdem verwenden?",
                            title="Passwortwarnung", font=("Segoe UI", 10))
                        if answer != "Yes":
                            continue
                    add_entry(fernet_obj, e_values['website'], e_values['username'], pwd, e_values['notes'])
                    sg.popup("Eintrag hinzugefügt", font=("Segoe UI", 10))
                    break
            entry_win.close()
            window["refresh"].click()
        elif event == "edit":
            selected = values["-TABLE-"]
            if not selected:
                sg.popup_error("Bitte wähle einen Eintrag aus!", font=("Segoe UI", 10))
                continue
            entries = get_all_entries(fernet_obj)
            entry_to_edit = entries[selected[0]]
            entry_win = entry_window(entry=entry_to_edit)
            while True:
                e_event, e_values = entry_win.read()
                if e_event in (sg.WINDOW_CLOSED, "Abbrechen"):
                    break
                # Echtzeit-Überprüfung im Bearbeitungsfenster:
                if e_event == "password":
                    pwd = e_values["password"]
                    try:
                        is_strong, breaches = check_password_strength(pwd)
                    except Exception as ex:
                        entry_win["pwd_strength"].update("Fehler bei API")
                        continue
                    if breaches > 0:
                        strength_text = f"Schwach ({breaches} gefunden)"
                        strength_color = "red"
                    else:
                        if len(pwd) < 8:
                            strength_text = "Schwach"
                            strength_color = "red"
                        elif len(pwd) < 12:
                            strength_text = "Normal"
                            strength_color = "yellow"
                        else:
                            strength_text = "Gut"
                            strength_color = "green"
                    entry_win["pwd_strength"].update(value=strength_text, text_color=strength_color)

                if e_event == "-GEN-":
                    gen_pw = generate_password()
                    entry_win["password"].update(gen_pw)
                    try:
                        is_strong, breaches = check_password_strength(gen_pw)
                    except Exception as ex:
                        entry_win["pwd_strength"].update("Fehler bei API")
                    else:
                        if breaches > 0:
                            strength_text = f"Schwach({breaches} treffer)"
                            strength_color = "red"
                        else:
                            if len(gen_pw) < 8:
                                strength_text = "Schwach"
                                strength_color = "red"
                            elif len(gen_pw) < 12:
                                strength_text = "gut"
                                strength_color = "yellow"
                            else:
                                strength_text = "Stark"
                                strength_color = "green"
                        entry_win["pwd_strength"].update(value=strength_text, text_color=strength_color)

                if e_event == "Speichern":
                    update_entry(fernet_obj, entry_to_edit['id'], e_values['website'], e_values['username'],
                                 e_values['password'], e_values['notes'])
                    sg.popup("Eintrag aktualisiert", font=("Segoe UI", 10))
                    break
            entry_win.close()
            window["refresh"].click()
        elif event == "-TABLE-DOUBLE-":
            # Analog zur Bearbeiten-Funktion
            selected = values["-TABLE-"]
            if not selected:
                continue
            entries = get_all_entries(fernet_obj)
            entry_to_edit = entries[selected[0]]
            entry_win = entry_window(entry=entry_to_edit)
            while True:
                e_event, e_values = entry_win.read()
                if e_event in (sg.WINDOW_CLOSED, "Abbrechen"):
                    break
                if e_event == "-GEN-":
                    gen_pw = generate_password()
                    entry_win["password"].update(gen_pw)
                if e_event == "Speichern":
                    update_entry(fernet_obj, entry_to_edit['id'], e_values['website'], e_values['username'],
                                 e_values['password'], e_values['notes'])
                    sg.popup("Eintrag aktualisiert", font=("Segoe UI", 10))
                    break
            entry_win.close()
            window["refresh"].click()
        elif event == "delete":
            selected = values["-TABLE-"]
            if not selected:
                sg.popup_error("Bitte wähle einen Eintrag aus!", font=("Segoe UI", 10))
                continue
            entries = get_all_entries(fernet_obj)
            entry_id = entries[selected[0]]['id']
            if sg.popup_yes_no("Soll der Eintrag wirklich gelöscht werden?", font=("Segoe UI", 10)) == "Yes":
                delete_entry(entry_id)
                sg.popup("Eintrag gelöscht", font=("Segoe UI", 10))
                window["refresh"].click()
        elif event == "gen_pw":
            new_pw = generate_password()
            is_strong, breaches = check_password_strength(new_pw)
            if is_strong:
                sg.popup("Generiertes Passwort: " + new_pw + "\nDas Passwort gilt als stark.", font=("Segoe UI", 10))
            else:
                sg.popup(
                    "Generiertes Passwort: " + new_pw + f"\nAchtung: Das Passwort wurde {breaches} mal gefunden und gilt als schwach.",
                    font=("Segoe UI", 10))

    window.close()


if __name__ == '__main__':
    main()
