from PyQt5.QtWidgets import QMainWindow, QWidget, QHeaderView, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QLineEdit, QPushButton, QAbstractItemView, QSizePolicy
from PyQt5.QtCore import Qt
from utils.ui_styles import apply_style
import pandas as pd

class FileContentView(QMainWindow):
    def __init__(self, dataframe=None):
        super().__init__()
        self.dataframe = dataframe
        self.setWindowTitle("Contenido del Archivo")
        self.init_ui()
        self.showMaximized()

    def init_ui(self):
        # Crear el widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Crear el layout principal
        main_layout = QVBoxLayout()

        # Crear el layout para el filtro de búsqueda
        search_layout = QHBoxLayout()
        search_label = QLabel("Buscar:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Ingrese texto para buscar en todas las columnas...")
        self.search_input.setFixedHeight(30)  # Ajustar altura del campo de búsqueda
        self.search_input.textChanged.connect(self.filter_table)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)

        # Crear la tabla
        self.table = QTableWidget()
        self.table.setColumnCount(self.dataframe.shape[1])
        self.table.setRowCount(len(self.dataframe))
        self.table.setHorizontalHeaderLabels(list(self.dataframe.columns))
        self.table.setSortingEnabled(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setAlternatingRowColors(True)  # Para mejorar la legibilidad

        # Aplicar estilo directamente al QTableWidget
        apply_style(self.table, "table_widget_style")

        # Llenar la tabla con los datos del DataFrame
        self.populate_table()

        # Ajustar el ancho de las columnas al contenido
        self.table.resizeColumnsToContents()

        # Ajustar manualmente el ancho de las columnas si es necesario
        header = self.table.horizontalHeader()
        for col in range(self.table.columnCount()):
            header.setSectionResizeMode(col, QHeaderView.ResizeToContents)

        # Botón de seleccionar/deseleccionar todo (opcional)
        # Puedes agregar botones adicionales si es necesario

        # Layout de botones (opcional)
        # button_layout = QHBoxLayout()
        # button_layout.addWidget(select_all_button)
        # button_layout.addWidget(export_button)
        # main_layout.addLayout(button_layout)

        # Agregar widgets al layout principal
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.table)
        central_widget.setLayout(main_layout)

    def populate_table(self):
        self.table.setRowCount(0)  # Limpiar la tabla antes de poblarla
        for row in range(len(self.dataframe)):
            self.table.insertRow(row)
            for col in range(self.dataframe.shape[1]):
                value = str(self.dataframe.iloc[row, col]) if pd.notna(self.dataframe.iloc[row, col]) else ""
                item = QTableWidgetItem(value)
                self.table.setItem(row, col, item)

    def filter_table(self):
        filter_text = self.search_input.text().lower()
        for row in range(self.table.rowCount()):
            match = False
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and filter_text in item.text().lower():
                    match = True
                    break
            self.table.setRowHidden(row, not match)