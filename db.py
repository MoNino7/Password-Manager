import sqlite3
import base64

DB_PATH = 'password_manager.db'

def get_connection():
    return sqlite3.connect(DB_PATH)

def initialize_db():
    conn = get_connection()
    cur = conn.cursor()
    # Tabelle für Einstellungen (z. B. Salt und Master-Verifier)
    cur.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    # Tabelle für Passwort-Einträge
    cur.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website TEXT,
            username TEXT,
            password TEXT,
            notes TEXT
        )
    ''')
    conn.commit()
    conn.close()

def set_setting(key, value):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('REPLACE INTO settings (key, value) VALUES (?,?)', (key, value))
    conn.commit()
    conn.close()

def get_setting(key):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT value FROM settings WHERE key=?', (key,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None
