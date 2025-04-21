# db_config_view.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox)
from PyQt5.QtCore import Qt
from utils.ui_styles import apply_style

class DBConfigView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        # Layout principal
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Título de la sección de configuración de la base de datos
        self.title_label = QLabel("Configuración de la Base de Datos", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        apply_style(self.title_label, "title_label")
        self.main_layout.addWidget(self.title_label)

        # Formulario de configuración
        self.form_layout = QVBoxLayout()
        self.main_layout.addLayout(self.form_layout)

        # Host
        self.host_layout = QHBoxLayout()
        self.host_label = QLabel("Host:", self)
        self.host_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.host_line_edit = QLineEdit(self)
        self.host_layout.addWidget(self.host_label)
        self.host_layout.addWidget(self.host_line_edit)
        self.form_layout.addLayout(self.host_layout)

        # Puerto
        self.port_layout = QHBoxLayout()
        self.port_label = QLabel("Puerto:", self)
        self.port_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.port_line_edit = QLineEdit(self)
        self.port_layout.addWidget(self.port_label)
        self.port_layout.addWidget(self.port_line_edit)
        self.form_layout.addLayout(self.port_layout)

        # Nombre de usuario
        self.username_layout = QHBoxLayout()
        self.username_label = QLabel("Usuario:", self)
        self.username_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.username_line_edit = QLineEdit(self)
        self.username_layout.addWidget(self.username_label)
        self.username_layout.addWidget(self.username_line_edit)
        self.form_layout.addLayout(self.username_layout)

        # Contraseña
        self.password_layout = QHBoxLayout()
        self.password_label = QLabel("Contraseña:", self)
        self.password_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.password_line_edit = QLineEdit(self)
        self.password_line_edit.setEchoMode(QLineEdit.Password)
        self.password_layout.addWidget(self.password_label)
        self.password_layout.addWidget(self.password_line_edit)
        self.form_layout.addLayout(self.password_layout)

        # Nombre de la base de datos
        self.database_layout = QHBoxLayout()
        self.database_label = QLabel("Base de Datos:", self)
        self.database_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.database_line_edit = QLineEdit(self)
        self.database_layout.addWidget(self.database_label)
        self.database_layout.addWidget(self.database_line_edit)
        self.form_layout.addLayout(self.database_layout)

        # Botones
        self.buttons_layout = QHBoxLayout()
        self.connect_button = QPushButton("Conectar", self)
        self.connect_button.clicked.connect(self.on_connect)
        self.save_button = QPushButton("Guardar Configuración", self)
        self.save_button.clicked.connect(self.on_save)
        self.buttons_layout.addWidget(self.connect_button)
        self.buttons_layout.addWidget(self.save_button)
        self.form_layout.addLayout(self.buttons_layout)

    def on_connect(self):
        # Obtener los datos de entrada
        host = self.host_line_edit.text()
        port = self.port_line_edit.text()
        username = self.username_line_edit.text()
        password = self.password_line_edit.text()
        database = self.database_line_edit.text()

        # Validar los datos (puedes agregar más validaciones aquí)
        if not host or not port or not username or not password or not database:
            QMessageBox.warning(self, "Advertencia", "Por favor, completa todos los campos.")
            return

        # Intentar la conexión a la base de datos
        try:
            # Aquí debes implementar la lógica de conexión a la base de datos
            # Por ejemplo:
            # connection = DatabaseConnection.connect(host, port, username, password, database)
            # if connection:
            #     QMessageBox.information(self, "Éxito", "Conexión exitosa.")
            # else:
            #     QMessageBox.warning(self, "Error", "No se pudo conectar a la base de datos.")
            QMessageBox.information(self, "Éxito", "Conexión simulada exitosa.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo conectar a la base de datos: {e}")

    def on_save(self):
        # Obtener los datos de entrada
        host = self.host_line_edit.text()
        port = self.port_line_edit.text()
        username = self.username_line_edit.text()
        password = self.password_line_edit.text()
        database = self.database_line_edit.text()

        # Validar los datos (puedes agregar más validaciones aquí)
        if not host or not port or not username or not password or not database:
            QMessageBox.warning(self, "Advertencia", "Por favor, completa todos los campos.")
            return

        # Guardar la configuración encriptada (implementar la lógica de encriptación)
        try:
            # Aquí debes implementar la lógica para guardar la configuración encriptada
            # Por ejemplo:
            # save_encrypted_config(host, port, username, password, database)
            QMessageBox.information(self, "Éxito", "Configuración guardada exitosamente.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo guardar la configuración: {e}")