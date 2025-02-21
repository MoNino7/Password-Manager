import PySimpleGUI as sg
from db import initialize_db
from crypto_utils import create_master_key
from gui import login_window, main_window, entry_window, show_message
from entries import get_all_entries, add_entry, update_entry, delete_entry, generate_password

def main():
    initialize_db()

    login_win = login_window()
    fernet_obj = None

    # Login-Schleife
    while True:
        event, values = login_win.read()
        if event in (sg.WINDOW_CLOSED, "Beenden"):
            login_win.close()
            return
        if event == "Login":
            master = values['master']
            fernet_obj = create_master_key(master)
            if fernet_obj is not None:
                sg.popup("Login erfolgreich!")
                break
            else:
                sg.popup_error("Falsches Master-Passwort!")
    login_win.close()

    main_win = main_window()

    while True:
        event, values = main_win.read()
        if event in (sg.WINDOW_CLOSED, "Beenden"):
            break
        elif event == "Aktualisieren":
            entries = get_all_entries(fernet_obj)
            table_values = [[e['id'], e['website'], e['username'], e['password'], e['notes']] for e in entries]
            main_win['-TABLE-'].update(values=table_values)
        elif event == "Neu":
            entry_win = entry_window()
            while True:
                e_event, e_values = entry_win.read()
                if e_event in (sg.WINDOW_CLOSED, "Abbrechen"):
                    break
                if e_event == "-GEN-":
                    gen_pw = generate_password()
                    entry_win['password'].update(gen_pw)
                if e_event == "Speichern":
                    add_entry(fernet_obj, e_values['website'], e_values['username'], e_values['password'], e_values['notes'])
                    sg.popup("Eintrag hinzugefügt")
                    break
            entry_win.close()
            main_win['Aktualisieren'].click()
        elif event == "Bearbeiten":
            selected = values['-TABLE-']
            if not selected:
                sg.popup_error("Bitte wähle einen Eintrag aus!")
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
                    entry_win['password'].update(gen_pw)
                if e_event == "Speichern":
                    update_entry(fernet_obj, entry_to_edit['id'], e_values['website'], e_values['username'], e_values['password'], e_values['notes'])
                    sg.popup("Eintrag aktualisiert")
                    break
            entry_win.close()
            main_win['Aktualisieren'].click()
        elif event == "Löschen":
            selected = values['-TABLE-']
            if not selected:
                sg.popup_error("Bitte wähle einen Eintrag aus!")
                continue
            entries = get_all_entries(fernet_obj)
            entry_id = entries[selected[0]]['id']
            if sg.popup_yes_no("Soll der Eintrag wirklich gelöscht werden?") == "Yes":
                delete_entry(entry_id)
                sg.popup("Eintrag gelöscht")
                main_win['Aktualisieren'].click()
        elif event == "Passwort generieren":
            new_pw = generate_password()
            sg.popup("Generiertes Passwort:", new_pw)
    main_win.close()

if __name__ == '__main__':
    main()
