# core/db_connection.py
import json
import os

class DatabaseConnection:
    def __init__(self):
        self.connection = None
        self.config = self.load_config()

    @staticmethod
    def _load_config_plain(config_path="config/db_config.json"):
        """Carga la configuración desde un archivo JSON sin encriptar."""
        if not os.path.exists(config_path):
            # Si el archivo no existe, devolver una configuración vacía
            return {}
        with open(config_path, "r") as file:
            config = json.load(file)
        return config

    @staticmethod
    def _save_config_plain(config, config_path="config/db_config.json"):
        """Guarda la configuración en un archivo JSON sin encriptar."""
        with open(config_path, "w") as file:
            json.dump(config, file, indent=4)

    def load_config(self):
        """Carga la configuración desde el archivo JSON."""
        return self._load_config_plain()

    def set_connection(self, connection_name):
        """Configura la conexión a la base de datos."""
        config = self.load_config()
        connection_info = config.get(connection_name, {})
        self.connection = connection_info

    @staticmethod
    def close_connection():
        """Cierra la conexión actual."""
        pass

    @staticmethod
    def get_connection():
        """Obtiene la conexión actual."""
        return DatabaseConnection().connection

    @staticmethod
    def _load_connection_names():
        """Carga los nombres de las conexiones desde la configuración."""
        config = DatabaseConnection._load_config_plain()
        return list(config.keys())

    @staticmethod
    def save_connection(connection_name, connection_info):
        """Guarda una nueva conexión o actualiza una existente."""
        config = DatabaseConnection._load_config_plain()
        config[connection_name] = connection_info
        DatabaseConnection._save_config_plain(config)