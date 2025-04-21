from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QFileDialog, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from views.file.file_content_view import FileContentView
from controllers.file.file_controller import FileController
from utils.ui_styles import apply_style


class FileView(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = None  # Se inicializará más adelante con `set_controller`
        self.init_ui()
        self.set_app_style()

    def init_ui(self):
        # Layout principal
        main_layout = QVBoxLayout()

        # Caja de texto para mostrar la ruta del archivo seleccionado
        self.file_path_label = QLineEdit(self)
        self.file_path_label.setPlaceholderText("Ruta del archivo...")
        self.file_path_label.setReadOnly(True)
        main_layout.addWidget(self.file_path_label)

        # Crear un layout horizontal para los botones
        buttons_layout = QHBoxLayout()

        # Botón para adquirir archivo
        self.acquire_button = QPushButton("Adquirir Archivo", self)
        self.acquire_button.clicked.connect(self.acquire_file)  # Conectar al método
        buttons_layout.addWidget(self.acquire_button)

        # Botón para ver los datos del archivo (inicialmente deshabilitado)
        self.view_data_button = QPushButton("Ver Datos", self)
        self.view_data_button.setEnabled(False)  # Deshabilitar al inicio
        self.view_data_button.clicked.connect(self.view_file_data)  # Conectar al método
        buttons_layout.addWidget(self.view_data_button)

        # Centrar los botones en el layout horizontal
        buttons_layout.setAlignment(Qt.AlignCenter)

        # Añadir el layout horizontal de botones al layout principal
        main_layout.addLayout(buttons_layout)

        # Establecer el layout principal
        self.setLayout(main_layout)

        # Configurar el controlador
        self.set_controller(FileController())  # No se pasa `self` como argumento

    def set_controller(self, controller):
        """
        Asocia un controlador a la vista y conecta sus señales a los métodos correspondientes.
        """
        self.controller = controller

        # Conectar las señales del controlador a los métodos de la vista
        self.controller.dataframe_loaded.connect(self.handle_dataframe_loaded)
        self.controller.error_occurred.connect(self.handle_error)
        self.controller.file_path_updated.connect(self.update_file_path)

    def set_app_style(self):
        apply_style(self, "main_window")

    def acquire_file(self):
        """
        Método para adquirir un archivo utilizando QFileDialog.
        """
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Archivo",
            "",
            "Archivos Excel y CSV (*.xls *.xlsx *.csv)"
        )

        # Si no se selecciona archivo, simplemente salir
        if not file_name:
            return

        # Mostrar la ruta del archivo en el campo de texto
        self.file_path_label.setText(file_name)

        # Intentar cargar el archivo utilizando el controlador
        self.controller.load_file(file_name)

    def view_file_data(self):
        """
        Método para ver los datos del archivo capturado.
        Este método abrirá la ventana de FileContentView con el contenido del dataframe.
        """
        self.show_file_content_view()

    def show_file_content_view(self):
        """
        Muestra la ventana secundaria con los datos del dataframe.
        """
        dataframe = self.controller.get_dataframe()  # Obtener el dataframe cargado

        if dataframe is not None and not dataframe.empty:
            self.content_view = FileContentView(dataframe)
            apply_style(self.content_view, "popup_window")
            self.content_view.show()  # Mostrar la ventana
        else:
            self.show_error_message("El archivo no contiene datos válidos para mostrar.")

    def enable_view_data_button(self):
        """
        Habilita el botón 'Ver Datos' cuando el archivo es válido.
        """
        self.view_data_button.setEnabled(True)

    def disable_view_data_button(self):
        """
        Deshabilita el botón 'Ver Datos'.
        """
        self.view_data_button.setEnabled(False)

    def handle_dataframe_loaded(self, success):
        """
        Maneja el evento de carga del DataFrame, actualizando la interfaz según el resultado.
        """
        if success:
            self.enable_view_data_button()
        else:
            self.disable_view_data_button()
            self.file_path_label.setText("")  # Limpiar la ruta del archivo

    def handle_error(self, message):
        """
        Maneja los errores emitidos por el controlador, mostrando un mensaje al usuario.
        """
        self.show_error_message(message)

    def show_error_message(self, message):
        """
        Muestra un mensaje de error al usuario.
        """
        QMessageBox.critical(self, "Error", message)

    def update_file_path(self, file_name):
        """
        Actualiza el nombre del archivo en la vista.
        """
        self.file_path_label.setText(f"Archivo cargado: {file_name}")
