# views/main_view.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame, QPushButton, QHBoxLayout, QComboBox, QMessageBox, QTabWidget)
from PyQt5.QtCore import Qt
from utils.ui_styles import apply_style
from views.table.table_view import TableView
from views.file.file_view import FileView
from views.management.manage_connections_dialog import ManageConnectionsDialog
from views.db_config.db_config_view import DBConfigView
from core.db_connection import DatabaseConnection
from views.management.import_view import ImportView

class MainView(QWidget):
    def __init__(self):
        super().__init__()

        # Crear una instancia de DatabaseConnection
        self.db_connection = DatabaseConnection()

        # Conectar la señal de cambio de conexión a un método
        self.db_connection.connection_changed.connect(self.update_connection_combo)

        # Layout principal
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Título de la aplicación
        self.init_title()

        # Barra de herramientas superior
        self.init_toolbar()

        # Bloques de vista
        self.init_blocks()

        # Botón para importar archivo
        self.init_import_button()

        # Estilo global para la aplicación
        self.set_app_style()

    def set_app_style(self):
        """Aplica un estilo global predefinido desde el diccionario de estilos."""
        apply_style(self, "main_window")

    def init_title(self):
        """Inicializa el título de la aplicación."""
        self.title_label = QLabel("REDLINE Collector", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        apply_style(self.title_label, "title_label")
        self.main_layout.addWidget(self.title_label)

    def init_toolbar(self):
        """Inicializa la barra de herramientas con el botón de administrar conexiones."""
        toolbar_layout = QHBoxLayout()

        # Combo box para seleccionar conexiones
        self.init_connection_combo()

        # Botón para administrar conexiones
        self.manage_connections_button = QPushButton("Administrar Conexiones")
        self.manage_connections_button.clicked.connect(self.manage_connections)
        toolbar_layout.addWidget(self.manage_connections_button)

        # Añadir el layout de la barra de herramientas al layout principal
        self.main_layout.addLayout(toolbar_layout)

    def init_connection_combo(self):
        """Inicializa el combo box para gestionar conexiones a la base de datos."""
        # Crear un layout horizontal para la etiqueta y el combo
        horizontal_layout = QHBoxLayout()

        # Crear la etiqueta para el combo
        self.connection_label = QLabel("Conexión:", self)
        self.connection_label.setObjectName("connection_label")
        self.connection_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)  # Alineación derecha y centrada verticalmente

        # Aplicar estilo a la etiqueta (negrita)
        self.connection_label.setStyleSheet("font-weight: bold; font-size: 14px;")

        # Añadir la etiqueta al layout horizontal
        horizontal_layout.addWidget(self.connection_label)

        # Crear el combo box para las conexiones
        self.connection_combo = QComboBox(self)
        self.connection_combo.setObjectName("connection_combo")
        self.connection_combo.addItem("")  # Elemento vacío inicial
        self.connection_combo.addItems(self.load_connection_names())
        self.connection_combo.currentIndexChanged.connect(self.on_connection_selected)

        # Añadir el combo box al layout horizontal
        horizontal_layout.addWidget(self.connection_combo)

        # Añadir el layout horizontal al layout principal
        self.main_layout.addLayout(horizontal_layout)

    def load_connection_names(self):
        """Carga los nombres de las conexiones desde la configuración JSON."""
        return DatabaseConnection._load_connection_names()

    def on_connection_selected(self):
        """Maneja el evento cuando se selecciona una nueva conexión en el combo box."""
        connection_name = self.connection_combo.currentText()
        if connection_name:
            self.db_connection.set_connection(connection_name)
            self.update_table_view()
        else:
            DatabaseConnection.close_connection()
            self.table_view.enable_table_controls(False)

    def init_blocks(self):
        """Inicializa los bloques principales de la vista."""
        self.blocks_widget = QTabWidget()
        self.blocks_layout = QVBoxLayout()
        self.blocks_widget.setLayout(self.blocks_layout)
        self.main_layout.addWidget(self.blocks_widget)

        self.init_table_block()
        self.init_file_block()
        self.init_db_config_block()

    def init_table_block(self):
        """Inicializa el bloque de tablas."""
        table_block = QWidget()
        table_block_layout = QVBoxLayout()
        table_block.setLayout(table_block_layout)

        title_label = QLabel("Bloque de Tablas", self)
        table_block_layout.addWidget(title_label)

        self.table_view = TableView()
        table_block_layout.addWidget(self.table_view)

        self.blocks_widget.addTab(table_block, "Tablas")

    def init_file_block(self):
        """Inicializa el bloque de archivos."""
        file_block = QWidget()
        file_block_layout = QVBoxLayout()
        file_block.setLayout(file_block_layout)

        title_label = QLabel("Archivo Colector", self)
        file_block_layout.addWidget(title_label)

        self.file_view = FileView()
        file_block_layout.addWidget(self.file_view)

        self.blocks_widget.addTab(file_block, "Archivos")

    def init_db_config_block(self):
        """Inicializa el bloque de configuración de la base de datos."""
        db_config_block = QWidget()
        db_config_block_layout = QVBoxLayout()
        db_config_block.setLayout(db_config_block_layout)

        self.db_config_view = DBConfigView(self)
        db_config_block_layout.addWidget(self.db_config_view)

        self.blocks_widget.addTab(db_config_block, "Configuración de la Base de Datos")

    def init_import_button(self):
        """Inicializa el botón 'Importar Archivo'."""
        self.import_button = QPushButton("Importar Archivo", self)
        self.import_button.setEnabled(False)
        self.import_button.clicked.connect(self.on_import_button_clicked)

        # Añadir el botón a la derecha del combo box de conexiones
        toolbar_layout = self.main_layout.itemAt(2).layout()
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.import_button)

        self.table_view.combo_box.currentIndexChanged.connect(self.update_import_button_status)
        self.file_view.controller.dataframe_loaded.connect(self.update_import_button_status)

    def update_import_button_status(self):
        """Actualiza el estado del botón 'Importar Archivo'."""
        table_selected = self.table_view.combo_box.currentText()
        dataframe = self.file_view.controller.get_dataframe()

        self.import_button.setEnabled(dataframe is not None and not dataframe.empty and bool(table_selected))

    def on_import_button_clicked(self):
        """Maneja el clic en el botón 'Importar Archivo'."""
        table_selected = self.table_view.combo_box.currentText()
        dataframe = self.file_view.controller.get_dataframe()

        if not dataframe.empty and table_selected:
            self.show_import_view(table_selected, dataframe)

    def show_import_view(self, table_selected, dataframe):
        """Muestra la vista de importación."""
        table_view = self.table_view
        self.import_view = ImportView(table_view, table_view, dataframe)
        self.import_view.show()

    def update_table_view(self):
        """Actualiza la vista de tablas cuando cambia la conexión."""
        connection = DatabaseConnection.get_connection()
        if connection:
            self.table_view.load_tables_for_connection(connection)
        else:
            self.table_view.enable_table_controls(False)

    def manage_connections(self):
        """Maneja el evento de clic en el botón 'Administrar Conexiones'."""
        dialog = ManageConnectionsDialog(self, config_path="config/db_config.json")
        dialog.exec_()