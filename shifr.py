from cryptography.fernet import Fernet
import hashlib

from config import key


def encrypt(data) -> str:
    cipher_suite = Fernet(key)
    encrypted_data = str(cipher_suite.encrypt(data.encode()))

    return encrypted_data[2:-1]


def decrypt(encrypted_data) -> str:
    cipher_suite = Fernet(key)
    data = bytes(encrypted_data, encoding='utf-8')
    decrypted_data = cipher_suite.decrypt(data).decode()
    return decrypted_data


def decrypt_data(row):
    data_dec = [[i[0], i[1], decrypt(i[2]), decrypt(i[3]), decrypt(i[4])] for i in row]
    return data_dec


def hash_data(data):
    md5_hash = hashlib.md5()
    md5_hash.update(data.encode())
    return md5_hash.hexdigest()
