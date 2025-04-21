import pandas as pd
from utils.ui_styles import apply_style
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, 
    QPushButton, QFileDialog, QMessageBox, QAbstractItemView, QSizePolicy, QLineEdit, QLabel
)
from PyQt5.QtCore import Qt

class TableDetailsView(QMainWindow):
    def __init__(self, table_name, table_structure, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Detalle de la tabla: {table_name}")

        self.table_name = table_name
        self.table_structure = table_structure if table_structure else []

        # Aplicar el estilo de la aplicación
        apply_style(self, "main_window")

        # Inicializar la interfaz gráfica
        self.init_ui()

        # Maximizar la ventana
        self.showMaximized()

    def init_ui(self):
        # Layout principal
        main_layout = QVBoxLayout()

        # Filtro de búsqueda
        search_layout = QHBoxLayout()
        search_label = QLabel("Buscar:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Ingrese texto para buscar en todas las columnas...")
        self.search_input.textChanged.connect(self.filter_table)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)

        # Tabla principal con las columnas de la tabla
        self.table = QTableWidget(self)
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["Columna", "Tipo de Dato", "PK", "Null?", "Constraints?", "Referencial?", "Seleccionar"])
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSortingEnabled(True)
        self.populate_table(self.table, self.table_structure)

        # Botón de seleccionar/deseleccionar todo
        self.select_all_button = QPushButton("Seleccionar todo")
        self.select_all_button.clicked.connect(self.toggle_select_all)

        # Botón de exportar
        export_button = QPushButton("Exportar")
        export_button.clicked.connect(self.export_to_excel)

        # Layout de botones
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.select_all_button)
        button_layout.addWidget(export_button)

        # Agregar widgets al layout principal
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.table)
        main_layout.addLayout(button_layout)

        # Contenedor principal
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def populate_table(self, table, structure):
        """
        Rellena la tabla con la estructura de la tabla.
        """
        table.setRowCount(0)
        if not structure:
            QMessageBox.warning(self, "Advertencia", "La estructura de la tabla está vacía.", QMessageBox.Ok)
            return

        for row, col_data in enumerate(structure):
            table.insertRow(row)

            for column, data in enumerate(col_data):
                # Verifica si los datos son None y los reemplaza por una cadena vacía
                if data is None:
                    data = ""
                table.setItem(row, column, QTableWidgetItem(str(data)))

            # Checkbox para seleccionar columnas
            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            checkbox_item.setCheckState(Qt.Unchecked)
            table.setItem(row, table.columnCount() - 1, checkbox_item)

        table.resizeColumnsToContents()

    def filter_table(self):
        """
        Filtra las filas de la tabla según el texto ingresado en el campo de búsqueda.
        """
        filter_text = self.search_input.text().lower()

        for row in range(self.table.rowCount()):
            match = False
            for column in range(self.table.columnCount() - 1):
                item = self.table.item(row, column)
                if item and filter_text in item.text().lower():
                    match = True
                    break

            self.table.setRowHidden(row, not match)

    def toggle_select_all(self):
        """
        Selecciona o deselecciona todas las columnas.
        """
        select_all = self.select_all_button.text() == "Seleccionar todo"
        for row in range(self.table.rowCount()):
            item = self.table.item(row, self.table.columnCount() - 1)
            if item:
                item.setCheckState(Qt.Checked if select_all else Qt.Unchecked)

        self.select_all_button.setText("Deseleccionar todo" if select_all else "Seleccionar todo")

    def export_to_excel(self):
        """
        Exporta las columnas seleccionadas a un archivo Excel.
        """
        selected_columns = []
        column_headers = []
        data_types = []

        for row in range(self.table.rowCount()):
            if self.table.item(row, self.table.columnCount() - 1).checkState() == Qt.Checked:
                column_headers.append(self.table.item(row, 0).text())  # Nombre de la columna
                data_types.append(self.table.item(row, 1).text())  # Tipo de dato

        if not column_headers:
            QMessageBox.warning(self, "Advertencia", "No hay columnas seleccionadas para exportar.", QMessageBox.Ok)
            return

        file_name, _ = QFileDialog.getSaveFileName(
            self, "Guardar archivo", f"Colector_{self.table_name}.xlsx", "Archivos Excel (*.xlsx)"
        )

        if file_name:
            # Crear un DataFrame con los encabezados y tipos de datos
            export_data = pd.DataFrame([column_headers, data_types])
            export_data.to_excel(file_name, index=False, header=False)
            QMessageBox.information(self, "Éxito", "Archivo exportado exitosamente.", QMessageBox.Ok)

