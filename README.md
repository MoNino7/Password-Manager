# Password Manager

Ein privater Desktop-Passwortmanager in Python. Dieses Projekt bietet:

- **Login mit Master-Passwort:**  
  Ein integriertes Login-Fenster, das in den Hauptbereich übergeht, sobald das richtige Master-Passwort eingegeben wurde.

- **Lokale Speicherung mit SQLite:**  
  Alle Daten werden in einer SQLite-Datenbank gesichert.

- **Sichere Verschlüsselung:**  
  Sensible Daten werden mit der [cryptography](https://cryptography.io)-Bibliothek verschlüsselt, inklusive Schlüsselableitung via PBKDF2.

- **Benutzerfreundliche GUI:**  
  Entwickelt mit [PySimpleGUI](https://pysimplegui.readthedocs.io/), mit Symbol-Buttons und Echtzeit-Passwortstärkeanzeige.

- **Passwortstärke-Check:**  
  Integration der Have I Been Pwned-API zur Überprüfung, ob ein Passwort bereits kompromittiert wurde. Die Stärke des Passworts wird in Echtzeit mittels Farbindikator (rot = schwach, gelb = normal, grün = gut) angezeigt – bereits während der Eingabe in den "Neuen" bzw. "Bearbeiten"-Fenstern.

---

## Features

- **Integrierter Login und Hauptfenster:**  
  Das Login erfolgt in einem einzigen Fenster, das bei erfolgreicher Authentifizierung den Hauptbereich mit CRUD-Funktionalitäten anzeigt.

- **CRUD-Funktionalität:**  
  - **Neu:** Erstelle neue Einträge mit Website, Username, Passwort und Notizen.
  - **Bearbeiten:** Bearbeite bestehende Einträge – auch per Doppelklick auf einen Tabelleneintrag.
  - **Löschen:** Entferne Einträge aus der Datenbank.
  - **Refresh:** Aktualisiere die Anzeige der gespeicherten Einträge.
  - **Passwort generieren:** Erstelle zufällig generierte Passwörter.

- **Echtzeit-Passwortstärkeanzeige:**  
  Sobald ein Passwort eingegeben oder generiert wird, zeigt ein Indikator dessen Stärke an. Falls das Passwort in Datenlecks gefunden wurde (über die Have I Been Pwned-API), wird es als schwach markiert.

---

## Installation

### Voraussetzungen

- **Python 3.12+**  
- **Virtual Environment** (optional, aber empfohlen)

### Installationsschritte

1. **Repository klonen:**

   ```bash
   git clone https://github.com/<dein-github-benutzername>/Passwort-Manager.git
   cd Passwort-Manager
   ```

2. **Virtuelle Umgebung erstellen (empfohlen):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Für Linux/Mac
   # oder
   venv\Scripts\activate      # Für Windows
   ```

3. **Abhängigkeiten installieren:**

   ```bash
   pip install -r requirements.txt
   ```

   *Falls keine `requirements.txt` vorhanden ist, installiere die folgenden Pakete:*

   ```bash
   pip install PySimpleGUI cryptography requests
   ```

---

## Verwendung

1. **Starten der Anwendung:**

   Stelle sicher, dass du in der virtuellen Umgebung bist (falls du eine verwendest), und starte die Anwendung:

   ```bash
   python main.py
   ```

2. **Login:**

   Gib dein Master-Passwort ein. Bei falscher Eingabe wird direkt im Login-Bereich eine Fehlermeldung angezeigt.

3. **Einträge verwalten:**

   - **Neuer Eintrag:**  
     Erstelle einen neuen Eintrag. Während der Eingabe wird die Passwortstärke in Echtzeit angezeigt.
     
   - **Bearbeiten:**  
     Wähle einen Eintrag aus der Tabelle und klicke auf das Bearbeitungs-Symbol oder doppelklicke auf einen Eintrag.
     
   - **Löschen:**  
     Wähle einen Eintrag aus und klicke auf das Lösch-Symbol.
     
   - **Refresh:**  
     Aktualisiere die Tabelle, um alle Einträge anzuzeigen.
     
   - **Passwort generieren:**  
     Klicke auf das Symbol, um ein neues, zufällig generiertes Passwort zu erhalten, inklusive einer Anzeige, ob es als stark oder schwach gilt.

---

## Dateistruktur

```
password_manager/
├── main.py                # Hauptanwendung, verbindet alle Module
├── db.py                  # Datenbank-Initialisierung und -Verbindung
├── crypto_utils.py        # Verschlüsselungsfunktionen (Schlüsselableitung, etc.)
├── entries.py             # CRUD-Funktionen für Passwort-Einträge und Passwortgenerierung
├── gui.py                 # GUI-Elemente und Fensterdefinitionen (inkl. entry_window)
├── requirements.txt       # (Optional) Abhängigkeitenliste
└── README.md              # Diese Datei
```

---

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Details findest du in der [LICENSE](LICENSE) Datei.

---

## Hinweise

- **API Limitierungen:**  
  Die Have I Been Pwned-API wird über das K-Anonymity-Verfahren verwendet. Bitte beachte die [Nutzungsbedingungen](https://haveibeenpwned.com/API/v3).

- **Sicherheit:**  
  Dieses Projekt dient als privater Prototyp. Für den produktiven Einsatz sollten zusätzliche Sicherheitsprüfungen, Tests und Code-Reviews erfolgen.

---

## Kontakt

Falls du Fragen oder Anregungen hast, kannst du gerne Issues im Repository eröffnen oder mich direkt kontaktieren.
