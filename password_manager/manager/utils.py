# manager/utils.py
from cryptography.fernet import Fernet
import os

def get_cipher():
    # Construye la ruta al archivo de la clave de forma segura
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    key_path = os.path.join(BASE_DIR, 'secret_key.txt')
    
    with open(key_path, 'rb') as key_file:
        key = key_file.read()
    
    return Fernet(key)