from PyQt5.QtWidgets import QMessageBox
from cryptography.fernet import Fernet
import json
import os

class ConfigManager:
    def __init__(self, config_path):
        self.config_path = config_path
        self.key_path = "config/key.key"
        self.generate_key_if_not_exists()
        self.cipher_suite = Fernet(self.load_key())

    def generate_key_if_not_exists(self):
        if not os.path.exists(self.key_path):
            key = Fernet.generate_key()
            with open(self.key_path, 'wb') as key_file:
                key_file.write(key)

    def load_key(self):
        return open(self.key_path, 'rb').read()

    def encrypt_config(self, data):
        encrypted_data = self.cipher_suite.encrypt(json.dumps(data).encode())
        with open(self.config_path, 'wb') as config_file:
            config_file.write(encrypted_data)

    def decrypt_config(self):
        try:
            with open(self.config_path, 'rb') as config_file:
                encrypted_data = config_file.read()
            decrypted_data = self.cipher_suite.decrypt(encrypted_data)
            return json.loads(decrypted_data.decode())
        except FileNotFoundError:
            QMessageBox.critical(None, "Error", f"No se encontró el archivo de configuración: {self.config_path}")
            return {}
        except Exception as e:
            QMessageBox.critical(None, "Error", f"No se pudo desencriptar el archivo de configuración: {e}")
            return {}