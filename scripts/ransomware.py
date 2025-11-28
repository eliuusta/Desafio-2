import os
from cryptography.fernet import Fernet

KEY_FILE = 'secret.key'

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as f:
        f.write(key)

def load_key():
    return open(KEY_FILE, 'rb').read()

def encrypt_file(filename):
    key = load_key()
    f = Fernet(key)
    with open(filename, 'rb') as file:
        data = file.read()
    encrypted = f.encrypt(data)
    with open(filename + '.encrypted', 'wb') as file:
        file.write(encrypted)

def decrypt_file(filename):
    key = load_key()
    f = Fernet(key)
    with open(filename, 'rb') as file:
        data = file.read()
    decrypted = f.decrypt(data)
    with open(filename.replace('.encrypted',''), 'wb') as file:
        file.write(decrypted)

if __name__ == '__main__':
    generate_key()
    for f in os.listdir('.'):
        if f.endswith('.txt'):
            encrypt_file(f)
