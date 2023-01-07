from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from pbkdf2 import PBKDF2

from model.List import List
from model.PasswordEntry import PasswordEntry


def list_all() -> [PasswordEntry]:
    all_password_entries = PasswordEntry.query.all()
    return all_password_entries


class PasswordEntryService:
    def __init__(self, database: SQLAlchemy):
        self.database = database

    def add(self, username: str, password: str, servicename: str, owner: str):
        new_entry = PasswordEntry(username, password, servicename, owner)
        self.database.session.add(new_entry)
        self.database.session.commit()

    def delete(self, entry_id: int) -> bool:
        existing_entry = PasswordEntry.query.get(entry_id)
        if existing_entry.owner == current_user.username or current_user.username == 'admin':
            self.database.session.delete(existing_entry)
            self.database.session.commit()
            return True
        return False

    def list_by_name(self, username) -> [PasswordEntry]:
        entries = self.database.session.query(PasswordEntry).filter(PasswordEntry.owner == username).all()
        return entries

    def encrypt_with(self, password: str, plaintext: str) -> bytes:
        salt = get_random_bytes(10)
        key = PBKDF2(password, salt).read(80)
        iv = key[0:16]
        cipher_key = key[16:48]
        mac_key = key[48:80]

        self.database.session.add(List(salt, mac_key, current_user.username))

        cipher = AES.new(cipher_key, AES.MODE_CBC, iv)

        return cipher.encrypt(plaintext.encode())

    def decrypt_with(self, password: str, ciphertext: bytes) -> str:
        list = self.database.session.get()
        key = PBKDF2(password, list.salt)
