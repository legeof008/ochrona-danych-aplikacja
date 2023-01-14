import bleach
import markdown
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from pbkdf2 import PBKDF2

from controller.service.UserHandlingService import is_logged
from model.PasswordEntry import PasswordEntry

allowed_tags = ["h1", "h2", "h3", "h4", "h5", "h6", "p", "strong", "em", "ol", "ul", "li",
                "nano"]


def list_all() -> [PasswordEntry]:
    all_password_entries = PasswordEntry.query.all()
    return all_password_entries


def get_hash_with(password: str, salt: bytes) -> bytes:
    password_hash = PBKDF2(password, salt).read(80)
    return password_hash


def encrypt_with(password: str, plaintext: str, salt: bytes) -> [bytes]:
    key = PBKDF2(password, salt).read(80)
    iv = key[0:16]
    cipher_key = key[16:48]
    mac_key = key[48:80]

    cipher = AES.new(cipher_key, AES.MODE_CBC, iv)
    difference = 16 - (len(plaintext) % 16)
    nonce = get_random_bytes(difference)
    full = plaintext.encode() + nonce
    cipher_text = cipher.encrypt(full)

    return [cipher_text, mac_key, difference]


def decrypt_with(username: str, password: str, ciphertext: bytes, salt: bytes, mac_key: bytes) -> bytes:
    key = PBKDF2(password + username, salt).read(80)
    iv = key[0:16]
    cipher_key = key[16:48]
    mac_key_current = key[48:80]

    cipher = AES.new(cipher_key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext


def authorized_with(request) -> bool:
    return request.args.get("token") and is_logged(int(request.args.get("token")))


class PasswordEntryService:
    def __init__(self, database: SQLAlchemy):
        self.database = database

    def add(self, username: str, password: str, special_password: str, servicename: str, owner: str):
        salt = get_random_bytes(10)
        html_plaintext = markdown.markdown(password)
        bleached_input = bleach.clean(html_plaintext, tags=allowed_tags)
        cipher_text, mac_key, nonce_len = encrypt_with(special_password + username, bleached_input, salt)
        new_entry = PasswordEntry(username, cipher_text, servicename, owner, salt, mac_key, nonce_len)
        self.database.session.add(new_entry)
        self.database.session.commit()

    def delete(self, entry_id: int) -> bool:
        existing_entry = PasswordEntry.query.get(entry_id)
        if existing_entry.owner == current_user.username:
            self.database.session.delete(existing_entry)
            self.database.session.commit()
            return True
        return False

    def list_by_name(self, username) -> [PasswordEntry]:
        entries = self.database.session.query(PasswordEntry).filter(PasswordEntry.owner == username).all()
        return entries

    def get(self, entry_id: int) -> PasswordEntry:
        return PasswordEntry.query.get(entry_id)
