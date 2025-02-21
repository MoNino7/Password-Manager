import secrets
from db import get_connection

def add_entry(f, website, username, password, notes):
    enc_password = f.encrypt(password.encode()).decode()
    enc_username = f.encrypt(username.encode()).decode()
    enc_notes = f.encrypt(notes.encode()).decode()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO entries (website, username, password, notes) VALUES (?,?,?,?)',
                (website, enc_username, enc_password, enc_notes))
    conn.commit()
    conn.close()

def get_all_entries(f):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, website, username, password, notes FROM entries')
    rows = cur.fetchall()
    conn.close()
    entries = []
    for row in rows:
        try:
            dec_username = f.decrypt(row[2].encode()).decode()
            dec_password = f.decrypt(row[3].encode()).decode()
            dec_notes = f.decrypt(row[4].encode()).decode()
        except Exception:
            dec_username = dec_password = dec_notes = "ERROR"
        entries.append({
            'id': row[0],
            'website': row[1],
            'username': dec_username,
            'password': dec_password,
            'notes': dec_notes
        })
    return entries

def update_entry(f, entry_id, website, username, password, notes):
    enc_password = f.encrypt(password.encode()).decode()
    enc_username = f.encrypt(username.encode()).decode()
    enc_notes = f.encrypt(notes.encode()).decode()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('UPDATE entries SET website=?, username=?, password=?, notes=? WHERE id=?',
                (website, enc_username, enc_password, enc_notes, entry_id))
    conn.commit()
    conn.close()

def delete_entry(entry_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM entries WHERE id=?', (entry_id,))
    conn.commit()
    conn.close()

def generate_password(length=12):
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
    return ''.join(secrets.choice(alphabet) for _ in range(length))
