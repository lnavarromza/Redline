from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox, QFormLayout
import json
import os
from PyQt5.QtCore import Qt
from core.db_connection import DatabaseConnection
from core.config_manager import ConfigManager

class AddEditConnectionDialog(QDialog):
    def __init__(self, parent=None, mode="add", config_manager=None, name="", host="", port="", service="", user=""):
        super().__init__(parent)
        self.setWindowTitle(f"{'Agregar' if mode == 'add' else 'Editar'} Conexión")
        self.setModal(True)
        self.mode = mode
        self.config_manager = config_manager
        self.name = name
        self.init_ui(host, port, service, user)

    def init_ui(self, host, port, service, user):
        layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.name_input = QLineEdit(self.name)
        self.host_input = QLineEdit(host)
        self.port_input = QLineEdit(port)
        self.service_input = QLineEdit(service)
        self.user_input = QLineEdit(user)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        form_layout.addRow("Nombre:", self.name_input)
        form_layout.addRow("Host:", self.host_input)
        form_layout.addRow("Puerto:", self.port_input)
        form_layout.addRow("Servicio:", self.service_input)
        form_layout.addRow("Usuario:", self.user_input)
        form_layout.addRow("Contraseña:", self.password_input)

        layout.addLayout(form_layout)

        # Botones
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Guardar")
        self.save_button.clicked.connect(self.save_connection)
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def save_connection(self):
        name = self.name_input.text()
        host = self.host_input.text()
        port = self.port_input.text()
        service = self.service_input.text()
        user = self.user_input.text()
        password = self.password_input.text()

        if not name or not host or not port or not service or not user:
            QMessageBox.warning(self, "Advertencia", "Todos los campos son obligatorios.")
            return

        try:
            decrypted_config = self.config_manager.decrypt_config()
            connections = decrypted_config.get("connections", {})
            if self.mode == "add":
                if name in connections:
                    QMessageBox.warning(self, "Advertencia", "El nombre de la conexión ya existe.")
                    return
                connections[name] = {
                    "host": host,
                    "port": int(port),
                    "service_name": service,
                    "user": user,
                    "password": password
                }
            else:
                if name != self.name:
                    del connections[self.name]
                connections[name] = {
                    "host": host,
                    "port": int(port),
                    "service_name": service,
                    "user": user,
                    "password": password
                }
            decrypted_config["connections"] = connections
            self.config_manager.encrypt_config(decrypted_config)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar la conexión: {e}")