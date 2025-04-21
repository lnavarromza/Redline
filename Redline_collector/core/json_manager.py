import os
import sys
import json

class JSONManager:
    """
    Clase para gestionar la lectura de archivos JSON, como db_config.json.
    """

    @staticmethod
    def get_config_path():
        """
        Devuelve la ruta del archivo JSON según el entorno (desarrollo o ejecutable).
        """
        if getattr(sys, 'frozen', False):  # Si está en un ejecutable
            base_path = os.path.dirname(os.path.abspath(sys.executable))
        else:  # Si está en desarrollo
            base_path = os.path.abspath(".")

        # Ajustar la ruta para que busque en 'config/db_config.json'
        return os.path.join(base_path, "config", "db_config.json")

    @staticmethod
    def load_connections(config_path=None):
        """
        Carga las conexiones desde el archivo JSON.
        :param config_path: Ruta del archivo JSON. Si no se proporciona, utiliza la ruta predeterminada.
        :return: Diccionario de conexiones.
        """
        if config_path is None:
            config_path = JSONManager.get_config_path()

        try:
            with open(config_path, "r") as file:
                data = json.load(file)
            return data.get("connections", {})
        except FileNotFoundError:
            print(f"Error: El archivo de configuración no se encontró en {config_path}.")
        except json.JSONDecodeError as e:
            print(f"Error al analizar el archivo JSON: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

        return {}

    @staticmethod
    def get_connection_details(connection_name, config_path=None):
        """
        Obtiene los detalles de una conexión específica desde el archivo JSON.
        :param connection_name: Nombre de la conexión.
        :param config_path: Ruta del archivo JSON. Si no se proporciona, utiliza la ruta predeterminada.
        :return: Diccionario con los detalles de la conexión o None si no se encuentra.
        """
        connections = JSONManager.load_connections(config_path)
        return connections.get(connection_name)

    @staticmethod
    def add_connection(connection_name, connection_details, file_path="db_config.json"):
        """
        Agrega una nueva conexión al archivo JSON.

        :param connection_name: Nombre de la nueva conexión.
        :param connection_details: Diccionario con los detalles de la conexión.
        :param file_path: Ruta del archivo JSON.
        """
        try:
            connections = JSONManager.load_connections(file_path) or {}
            if connection_name in connections:
                print(f"La conexión '{connection_name}' ya existe. No se puede sobrescribir.")
                return

            connections[connection_name] = connection_details

            with open(file_path, "w") as file:
                json.dump({"connections": connections}, file, indent=4)
            print(f"Conexión '{connection_name}' agregada correctamente.")
        except Exception as e:
            print(f"Error al agregar la conexión: {e}")

    @staticmethod
    def delete_connection(connection_name, file_path="db_config.json"):
        """
        Elimina una conexión específica del archivo JSON.

        :param connection_name: Nombre de la conexión a eliminar.
        :param file_path: Ruta del archivo JSON.
        """
        try:
            connections = JSONManager.load_connections(file_path) or {}
            if connection_name not in connections:
                print(f"La conexión '{connection_name}' no existe. No se puede eliminar.")
                return

            del connections[connection_name]

            with open(file_path, "w") as file:
                json.dump({"connections": connections}, file, indent=4)
            print(f"Conexión '{connection_name}' eliminada correctamente.")
        except Exception as e:
            print(f"Error al eliminar la conexión: {e}")

    @staticmethod
    def update_connection(connection_name, updated_details, file_path="db_config.json"):
        """
        Actualiza los detalles de una conexión existente en el archivo JSON.

        :param connection_name: Nombre de la conexión a actualizar.
        :param updated_details: Diccionario con los nuevos detalles de la conexión.
        :param file_path: Ruta del archivo JSON.
        """
        try:
            connections = JSONManager.load_connections(file_path) or {}
            if connection_name not in connections:
                print(f"La conexión '{connection_name}' no existe. No se puede actualizar.")
                return

            connections[connection_name] = updated_details

            with open(file_path, "w") as file:
                json.dump({"connections": connections}, file, indent=4)
            print(f"Conexión '{connection_name}' actualizada correctamente.")
        except Exception as e:
            print(f"Error al actualizar la conexión: {e}")
