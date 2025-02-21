import PySimpleGUI as sg
from db import initialize_db
from crypto_utils import create_master_key
from entries import get_all_entries, add_entry, update_entry, delete_entry, generate_password
from gui import entry_window

def main():
    initialize_db()
    sg.theme("SystemDefault")

    # Definiere den Login-Bereich
    login_column = [
        [sg.Text("Bitte Master-Passwort eingeben:", font=("Segoe UI", 12))],
        [sg.Input(password_char="*", key="master", font=("Segoe UI", 12))],
        [sg.Text("", key="error", size=(40, 1), text_color="red", font=("Segoe UI", 10))],
        [sg.Button("Login", key="login_btn", font=("Segoe UI", 12))]
    ]

    # Definiere den Hauptbereich mit Symbol-Buttons neben der Tabelle
    main_column = [
        [sg.Table(values=[], headings=["ID", "Website", "Username", "Passwort", "Notizen"],
                  key="-TABLE-", auto_size_columns=True, display_row_numbers=False,
                  num_rows=10, enable_events=True, font=("Segoe UI", 10))],
        [sg.Button("➕", key="new", tooltip="Neuer Eintrag", font=("Segoe UI", 12), border_width=0, pad=(5,5)),
         sg.Button("✏️", key="edit", tooltip="Bearbeiten", font=("Segoe UI", 12), border_width=0, pad=(5,5)),
         sg.Button("🗑️", key="delete", tooltip="Löschen", font=("Segoe UI", 12), border_width=0, pad=(5,5)),
         sg.Button("🔄", key="refresh", tooltip="Aktualisieren", font=("Segoe UI", 12), border_width=0, pad=(5,5)),
         sg.Button("🔑", key="gen_pw", tooltip="Passwort generieren", font=("Segoe UI", 12), border_width=0, pad=(5,5)),
         sg.Button("Beenden", key="exit", font=("Segoe UI", 12))]
    ]

    # Layout: Login-Bereich sichtbar, Hauptbereich ausgeblendet
    layout = [[
        sg.Column(login_column, key="login_col", element_justification="center"),
        sg.Column(main_column, key="main_col", visible=False)
    ]]

    window = sg.Window("YourKey", layout, finalize=True, resizable=True)
    window.bind("<Return>", "login_enter")
    table_elem = window["-TABLE-"]
    table_elem.Widget.bind("<Double-Button-1>", lambda event: window.write_event_value('-TABLE-DOUBLE-', event))

    # Zentriere das Fenster manuell mit deinen Werten
    root = window.TKroot
    root.update_idletasks()  # Aktualisiere Geometrie-Daten
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

        # Login-Phase
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

        # Hauptbereich
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
                if e_event == "-GEN-":
                    gen_pw = generate_password()
                    entry_win["password"].update(gen_pw)
                if e_event == "Speichern":
                    add_entry(fernet_obj, e_values['website'], e_values['username'], e_values['password'], e_values['notes'])
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
                if e_event == "-GEN-":
                    gen_pw = generate_password()
                    entry_win["password"].update(gen_pw)
                if e_event == "Speichern":
                    update_entry(fernet_obj, entry_to_edit['id'], e_values['website'], e_values['username'], e_values['password'], e_values['notes'])
                    sg.popup("Eintrag aktualisiert", font=("Segoe UI", 10))
                    break
            entry_win.close()
            window["refresh"].click()
        elif event == "-TABLE-DOUBLE-":
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
                    update_entry(fernet_obj, entry_to_edit['id'], e_values['website'], e_values['username'], e_values['password'], e_values['notes'])
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
            sg.popup("Generiertes Passwort: " + new_pw, font=("Segoe UI", 10))

    window.close()

if __name__ == '__main__':
    main()
