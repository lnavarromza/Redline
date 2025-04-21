import pandas as pd
from csv import Sniffer
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton


class FileController(QObject):
    # Señales para comunicar eventos a la vista
    dataframe_loaded = pyqtSignal(bool)  # Notifica si el dataframe fue cargado correctamente
    error_occurred = pyqtSignal(str)  # Notifica que ocurrió un error y envía el mensaje
    file_path_updated = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.dataframe = None  # Inicialmente no hay `DataFrame`

    def load_file(self, file_name, selected_sheet=None):
        try:
            # Intentar cargar el archivo según su extensión
            if file_name.endswith(".xls"):
                self.dataframe = pd.read_excel(file_name, engine="xlrd")  # `.xls` requiere `xlrd`
            elif file_name.endswith(".xlsx"):
                with pd.ExcelFile(file_name, engine="openpyxl") as excel_file:
                    if len(excel_file.sheet_names) > 1 and selected_sheet is None:
                        self.show_sheet_selector_dialog(file_name, excel_file.sheet_names)
                        return
                    sheet_to_load = selected_sheet if selected_sheet else excel_file.sheet_names[0]
                    self.dataframe = pd.read_excel(excel_file, sheet_name=sheet_to_load)
                    self.file_path_updated.emit(f"{file_name} ({sheet_to_load})")
            elif file_name.endswith(".csv"):
                # Detectar automáticamente el delimitador del CSV
                with open(file_name, "r", encoding="utf-8") as file:
                    sample = file.read(2048)  # Leer una muestra del archivo
                    dialect = Sniffer().sniff(sample)  # Detectar el delimitador
                    file.seek(0)  # Volver al inicio del archivo
                    self.dataframe = pd.read_csv(file, delimiter=dialect.delimiter)
                self.file_path_updated.emit(file_name)
            else:
                raise ValueError("Formato de archivo no soportado. Use .xls, .xlsx o .csv.")

            # Reemplazar NaN por None
            self.dataframe = self.dataframe.where(pd.notnull(self.dataframe), None)

            if self.dataframe.empty:
                raise ValueError("El archivo cargado no contiene datos.")

            self.dataframe_loaded.emit(True)
        except Exception as e:
            self.dataframe = None
            self.error_occurred.emit(f"Error al cargar el archivo: {str(e)}")
            self.dataframe_loaded.emit(False)

    def show_sheet_selector_dialog(self, file_name, sheet_names):
        """
        Muestra un cuadro de diálogo para que el usuario seleccione una hoja del archivo.
        """
        dialog = QDialog()
        dialog.setWindowTitle("Seleccionar Hoja")

        layout = QVBoxLayout()
        label = QLabel("El archivo tiene varias hojas. Seleccione una hoja para cargar:")
        layout.addWidget(label)

        sheet_selector = QComboBox(dialog)
        sheet_selector.addItems(sheet_names)
        layout.addWidget(sheet_selector)

        accept_button = QPushButton("Aceptar", dialog)
        accept_button.clicked.connect(
            lambda: self.load_selected_sheet(dialog, sheet_selector, file_name)
        )
        layout.addWidget(accept_button)

        cancel_button = QPushButton("Cancelar", dialog)
        cancel_button.clicked.connect(dialog.reject)
        layout.addWidget(cancel_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def load_selected_sheet(self, dialog, sheet_selector, file_name):
        """
        Carga la hoja seleccionada por el usuario y cierra el cuadro de diálogo.
        """
        selected_sheet = sheet_selector.currentText()
        dialog.accept()
        self.load_file(file_name, selected_sheet)

    def get_dataframe(self):
        """
        Retorna el `DataFrame` cargado.
        """
        if self.dataframe is not None:
            self.dataframe = self.dataframe.where(pd.notnull(self.dataframe), None)
            self.dataframe = self.dataframe.dropna(how="all")
            self.dataframe = self.dataframe.astype(object)

        return self.dataframe

    def clean_up_on_error(self):
        """
        Limpia el estado del controlador en caso de error.
        """
        self.dataframe = None
        self.dataframe_loaded.emit(False)
