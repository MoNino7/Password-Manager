import base64
import secrets
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from db import get_setting, set_setting

VERIFIER_PLAINTEXT = b"verified"  # Zum Überprüfen des Master-Passworts

def derive_key(master_password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    return key

def create_master_key(master_password: str) -> Fernet:
    salt = get_setting('salt')
    if salt is None:
        # Erster Start: Salt generieren und speichern
        salt = secrets.token_bytes(16)
        set_setting('salt', base64.b64encode(salt).decode())
        key = derive_key(master_password, salt)
        f = Fernet(key)
        # Master verifier verschlüsseln und speichern
        verifier = f.encrypt(VERIFIER_PLAINTEXT)
        set_setting('master_verifier', verifier.decode())
        return f
    else:
        salt = base64.b64decode(salt.encode())
        key = derive_key(master_password, salt)
        f = Fernet(key)
        stored_verifier = get_setting('master_verifier')
        try:
            decrypted = f.decrypt(stored_verifier.encode())
            if decrypted == VERIFIER_PLAINTEXT:
                return f
            else:
                return None
        except Exception:
            return None
