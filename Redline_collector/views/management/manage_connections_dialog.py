# views/management/add_edit_connection_dialog.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QComboBox, QMessageBox
from PyQt5.QtCore import Qt
from core.config_manager import ConfigManager

class AddEditConnectionDialog(QDialog):
    def __init__(self, parent=None, mode="add", config_manager=None, name="", host="", port="", service="", user=""):
        super().__init__(parent)
        self.mode = mode
        self.config_manager = config_manager
        self.name = name
        self.host = host
        self.port = port
        self.service = service
        self.user = user
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"{'Agregar' if self.mode == 'add' else 'Editar'} Conexión")
        layout = QVBoxLayout()

        # Formulario de conexión
        form_layout = QVBoxLayout()

        # Nombre
        name_layout = QHBoxLayout()
        name_label = QLabel("Nombre:", self)
        name_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.name_line_edit = QLineEdit(self)
        self.name_line_edit.setText(self.name)
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_line_edit)
        form_layout.addLayout(name_layout)

        # Host
        host_layout = QHBoxLayout()
        host_label = QLabel("Host:", self)
        host_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.host_line_edit = QLineEdit(self)
        self.host_line_edit.setText(self.host)
        host_layout.addWidget(host_label)
        host_layout.addWidget(self.host_line_edit)
        form_layout.addLayout(host_layout)

        # Puerto
        port_layout = QHBoxLayout()
        port_label = QLabel("Puerto:", self)
        port_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.port_line_edit = QLineEdit(self)
        self.port_line_edit.setText(self.port)
        port_layout.addWidget(port_label)
        port_layout.addWidget(self.port_line_edit)
        form_layout.addLayout(port_layout)

        # Servicio
        service_layout = QHBoxLayout()
        service_label = QLabel("Servicio:", self)
        service_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.service_line_edit = QLineEdit(self)
        self.service_line_edit.setText(self.service)
        service_layout.addWidget(service_label)
        service_layout.addWidget(self.service_line_edit)
        form_layout.addLayout(service_layout)

        # Usuario
        user_layout = QHBoxLayout()
        user_label = QLabel("Usuario:", self)
        user_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.user_line_edit = QLineEdit(self)
        self.user_line_edit.setText(self.user)
        user_layout.addWidget(user_label)
        user_layout.addWidget(self.user_line_edit)
        form_layout.addLayout(user_layout)

        layout.addLayout(form_layout)

        # Botones
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("Aceptar")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def accept(self):
        # Obtener los datos de entrada
        name = self.name_line_edit.text()
        host = self.host_line_edit.text()
        port = self.port_line_edit.text()
        service = self.service_line_edit.text()
        user = self.user_line_edit.text()

        # Validar los datos (puedes agregar más validaciones aquí)
        if not name or not host or not port or not service or not user:
            QMessageBox.warning(self, "Advertencia", "Por favor, completa todos los campos.")
            return

        # Guardar la configuración
        connections = self.config_manager.get_connections()
        if self.mode == "add":
            connections[name] = {
                "host": host,
                "port": port,
                "service_name": service,
                "user": user
            }
        elif self.mode == "edit":
            connections[name] = {
                "host": host,
                "port": port,
                "service_name": service,
                "user": user
            }
        self.config_manager.set_connections(connections)
        super().accept()