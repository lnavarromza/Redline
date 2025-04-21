from views.dialogs.progress_dialog import ProgressDialog
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QAbstractItemView
)
from PyQt5.QtCore import QTimer, QCoreApplication, Qt
from controllers.management.import_controller import ImportController
from utils.ui_styles import apply_style

class ImportView(QWidget):
    def __init__(self, table_view, table_name, dataframe):
        super().__init__()
        self.table_name = table_name
        self.dataframe = dataframe
        self.table_view = table_view

        # Instanciar el controlador de la tabla
        table_controller = self.table_view.controller
        self.import_controller = ImportController(table_controller, dataframe)

        self.setWindowTitle("Importación de Archivos")
        self.init_ui()
        self.set_app_style()

        # Iniciar la ventana maximizada
        self.showMaximized()

    def init_ui(self):
        """
        Configura los elementos principales de la interfaz.
        """
        layout = QVBoxLayout()

        # Crear la grilla para mostrar la estructura de la tabla y validaciones
        self.table_widget = QTableWidget()
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.setSortingEnabled(True)
        layout.addWidget(self.table_widget, stretch=2)

        # Crear la grilla para registros omitidos
        self.omitted_grid = QTableWidget()
        self.omitted_grid.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.omitted_grid.setSortingEnabled(True)
        layout.addWidget(self.omitted_grid, stretch=1)

        # Cargar la estructura de la tabla y validaciones
        self.load_table_structure()

        # Botón para iniciar la importación
        self.import_button = QPushButton("Importar Datos", self)
        self.import_button.clicked.connect(self.import_data)
        layout.addWidget(self.import_button, 0, Qt.AlignmentFlag.AlignHCenter)

        self.setLayout(layout)

        # Ajustar tamaño de columnas y filas
        QTimer.singleShot(0, self.table_widget.resizeColumnsToContents)
        QTimer.singleShot(0, self.omitted_grid.resizeColumnsToContents)

    def set_app_style(self):
        """
        Aplica los estilos de la aplicación.
        """
        apply_style(self, "main_window")

    def load_table_structure(self):
        """
        Carga la estructura de la tabla en la grilla principal y realiza las validaciones.
        """
        self.table_widget.setUpdatesEnabled(False)

        # Obtener la estructura de las columnas desde el controlador
        columns = self.import_controller.load_table_structure(self.table_name)

        # Configurar la tabla con el número de filas y columnas necesarias
        self.table_widget.setRowCount(len(columns))
        self.table_widget.setColumnCount(5)  # Columnas: Nombre, Tipo, En Planilla, Validación, Errores

        # Encabezados de la tabla
        self.table_widget.setHorizontalHeaderLabels(
            ["Nombre de Columna", "Tipo de Dato", "En Planilla", "Validación", "Errores"]
        )

        # Crear lista con columnas coincidentes y datos únicos
        dataframe_columns = set(self.dataframe.columns)
        visible_columns = [
            {"column_name": col["column_name"], "data": self.dataframe[col["column_name"]].drop_duplicates()}
            for col in columns if col["column_name"] in dataframe_columns
        ]

        # Validar columnas y obtener resultados
        validation_results = self.import_controller.validate_columns(visible_columns, self.table_name)

        # Llenar la grilla principal con los resultados de validación
        for i, column in enumerate(columns):
            column_name = column["column_name"]
            column_type = column["data_type_formatted"]

            self.table_widget.setItem(i, 0, QTableWidgetItem(column_name))
            self.table_widget.setItem(i, 1, QTableWidgetItem(column_type))
            self.table_widget.setItem(i, 2, QTableWidgetItem("En Planilla" if column_name in dataframe_columns else "No Disponible"))

            validation_status = next(
                (result["status"] for result in validation_results if result["column_name"] == column_name), "No Validado"
            )
            error_rows = next(
                (result["errores"] for result in validation_results if result["column_name"] == column_name), "Ningún error"
            )
            self.table_widget.setItem(i, 3, QTableWidgetItem(validation_status))
            self.table_widget.setItem(i, 4, QTableWidgetItem(str(error_rows)))

        # Configurar la grilla de omitidos
        matching_columns = [col["column_name"] for col in columns if col["column_name"] in dataframe_columns]
        self.setup_omitted_grid(matching_columns)

        self.table_widget.setUpdatesEnabled(True)
        QTimer.singleShot(0, self.table_widget.resizeColumnsToContents)

    def setup_omitted_grid(self, matching_columns):
        """
        Configura la grilla para mostrar registros omitidos.
        """
        self.omitted_grid.setColumnCount(len(matching_columns) + 1)  # Columnas + Errores
        self.omitted_grid.setHorizontalHeaderLabels(matching_columns + ["Errores"])
        QTimer.singleShot(0, self.omitted_grid.resizeColumnsToContents)

    def import_data(self):
        """
        Inicia el proceso de importación de datos y gestiona la interacción con la vista.
        """
        try:
            # Crear y mostrar el ProgressDialog
            total_records = len(self.dataframe)
            progress_dialog = ProgressDialog(total_records, self)
            progress_dialog.show()

            # Conectar la señal de cancelación
            progress_dialog.cancel_signal.connect(self.import_controller.cancel)

            # Callback para manejar registros omitidos
            def on_omitted(omitted_record):
                self.add_omitted_record(omitted_record)

            # Callback para actualizar la barra de progreso
            def on_progress_update(processed, total):
                progress_dialog.update_progress(processed)
                QCoreApplication.processEvents()  # Mantener la UI responsiva

            # Llamar al controlador para importar datos
            result = self.import_controller.import_data(
                table_name=self.table_name,
                columns_to_insert=self.get_columns_to_insert(self.import_controller.get_table_columns(self.table_name)),
                on_omitted_callback=on_omitted,
                progress_callback=on_progress_update
            )

            # Cerrar el diálogo de progreso al finalizar
            progress_dialog.close_dialog()

            # Mostrar un resumen del proceso
            if result["cancelled"]:
                QMessageBox.warning(
                    self,
                    "Importación cancelada",
                    f"El proceso de importación fue cancelado.\n"
                    f"Registros insertados: {result['inserted']}\n"
                    f"Registros omitidos: {result['errors']}"
                )
            else:
                QMessageBox.information(
                    self,
                    "Importación completada",
                    f"Registros insertados: {result['inserted']}\n"
                    f"Registros omitidos: {result['errors']}"
                )

        except Exception as e:
            QMessageBox.critical(self, "Error crítico", f"Se produjo un error durante la importación: {e}")

    def get_columns_to_insert(self, columns):
        """
        Obtiene las columnas comunes entre la tabla y el DataFrame.
        """
        dataframe_columns = set(self.dataframe.columns)
        visible_columns = [col["column_name"] for col in columns if col["column_name"] in dataframe_columns]

        if not visible_columns:
            QMessageBox.warning(
                self,
                "Sin columnas coincidentes",
                "No hay columnas comunes entre la tabla seleccionada y el archivo cargado. No hay datos para importar."
            )
            return []
        return visible_columns

    def add_omitted_record(self, record):
        """
        Agrega un registro omitido a la grilla de omitidos.
        """
        row_count = self.omitted_grid.rowCount()
        self.omitted_grid.insertRow(row_count)
        for col_idx, (key, value) in enumerate(record.items()):
            self.omitted_grid.setItem(row_count, col_idx, QTableWidgetItem(str(value)))

        self.omitted_grid.resizeColumnsToContents()
