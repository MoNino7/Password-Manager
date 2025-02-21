import PySimpleGUI as sg
from entries import get_all_entries, add_entry, update_entry, delete_entry, generate_password

def login_window():
    layout = [
        [sg.Text("Bitte Master-Passwort eingeben:", font=("Segoe UI", 12))],
        [sg.Input(password_char="*", key="master", font=("Segoe UI", 12))],
        [sg.Text("", key="error", size=(40, 1), text_color="red", font=("Segoe UI", 10))],
        [sg.Button("Login", key="login_btn", font=("Segoe UI", 12))]
    ]
    window = sg.Window("Login", layout, finalize=True)
    # Binde die Enter-Taste an ein eigenes Event "login_enter"
    window.bind("<Return>", "login_enter")
    return window


def main_window():
    table_data = []
    headings = ["ID", "Website", "Username", "Passwort", "Notizen"]
    layout = [
        [sg.Table(values=table_data, headings=headings, key='-TABLE-', auto_size_columns=True,
                  display_row_numbers=False, num_rows=10, enable_events=True)],
        [sg.Button("Neu"), sg.Button("Bearbeiten"), sg.Button("Löschen"),
         sg.Button("Passwort generieren"), sg.Button("Aktualisieren"), sg.Button("Beenden")]
    ]
    return sg.Window("Password Manager", layout, finalize=True)

def entry_window(entry=None):
    layout = [
        [sg.Text("Website:"), sg.Input(entry['website'] if entry else "", key='website')],
        [sg.Text("Username:"), sg.Input(entry['username'] if entry else "", key='username')],
        [sg.Text("Passwort:"),
         sg.Input(entry['password'] if entry else "", key='password', enable_events=True)],
        [sg.Text("Stärke: "), sg.Text("Noch nicht geprüft", key="pwd_strength", size=(20,1), font=("Segoe UI", 10))],
        [sg.Button("Generiere Passwort", key='-GEN-')],
        [sg.Text("Notizen:"), sg.Multiline(entry['notes'] if entry else "", key='notes', size=(40, 5))],
        [sg.Button("Speichern"), sg.Button("Abbrechen")]
    ]
    return sg.Window("Eintrag", layout, modal=True, finalize=True)
def show_message(title, message):
    sg.popup(title, message)
