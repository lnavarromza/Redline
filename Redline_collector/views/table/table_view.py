from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QComboBox, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from controllers.table.table_controller import TableController
from views.table.table_details_view import TableDetailsView
from core.db_connection import DatabaseConnection

class TableView(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = None  # El controlador se configura en init_ui
        self.init_ui()

    def init_ui(self):
        # Layout principal horizontal para alinear los componentes
        main_layout = QHBoxLayout()

        # Contenedor para la caja de búsqueda y el combo (a la izquierda)
        left_layout = QVBoxLayout()

        # Caja de búsqueda
        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText("Filtrar tablas...")
        self.search_box.setEnabled(False)  # Deshabilitar al inicio
        left_layout.addWidget(self.search_box)

        # ComboBox para mostrar las tablas
        self.combo_box = QComboBox(self)
        self.combo_box.setEnabled(False)  # Deshabilitar al inicio
        left_layout.addWidget(self.combo_box)

        # Añadir el contenedor izquierdo al layout principal
        main_layout.addLayout(left_layout)

        # Contenedor para el botón "Mostrar Tabla" (a la derecha)
        right_layout = QVBoxLayout()

        # Botón Mostrar tabla
        self.show_table_button = QPushButton("Mostrar Tabla", self)
        self.show_table_button.setEnabled(False)  # Deshabilitar al inicio
        self.show_table_button.clicked.connect(self.show_table_details)
        right_layout.addWidget(self.show_table_button)

        # Centrar el botón verticalmente
        right_layout.setAlignment(self.show_table_button, Qt.AlignVCenter)

        # Añadir el contenedor derecho al layout principal
        main_layout.addLayout(right_layout)

        # Establecer el layout principal
        self.setLayout(main_layout)

        # Configurar el controlador
        self.set_controller(TableController(self))

    def set_controller(self, controller):
        self.controller = controller
        self.search_box.textChanged.connect(self.controller.filter_tables)

    def initialize_connection(self):
        """
        Carga las tablas de la conexión activa gestionada por DatabaseConnection.
        """
        connection = DatabaseConnection.get_connection()
        if connection:
            self.controller.connect_and_load_tables(connection)
        else:
            self.enable_table_controls(False)

    def enable_table_controls(self, enabled):
        """
        Habilita o deshabilita los controles relacionados con las tablas.
        """
        self.combo_box.setEnabled(enabled)
        self.search_box.setEnabled(enabled)
        self.show_table_button.setEnabled(enabled)

    def populate_combo_box(self, tables):
        """
        Llena el combo box con la lista de tablas.
        """
        self.combo_box.clear()
        self.combo_box.addItems(tables)

    def show_table_details(self):
        """
        Muestra los detalles de la tabla seleccionada en una nueva ventana.
        """
        table_name = self.combo_box.currentText()
        if table_name:
            table_structure = self.controller.get_table_structure(table_name)
            self.details_window = TableDetailsView(table_name, table_structure)
            self.details_window.show()

    def load_tables_for_connection(self, connection):
        try:
            # Llamamos al método correcto para cargar las tablas, sin pasar el argumento de conexión
            self.controller.connect_and_load_tables()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar las tablas: {e}")


