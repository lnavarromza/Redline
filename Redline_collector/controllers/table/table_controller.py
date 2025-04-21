from models.table.table_model import TableModel
from core.db_connection import DatabaseConnection
from PyQt5.QtCore import QCoreApplication
from views.dialogs.progress_dialog import ProgressDialog

class TableController:
    def __init__(self, view):
        """
        Inicializa el controlador de tablas.
        :param view: La vista asociada al controlador.
        """
        self.view = view
        self.model = TableModel()  # Modelo que gestiona las operaciones de base de datos
        self.all_tables = []  # Lista local para almacenar las tablas cargadas

    def connect_and_load_tables(self):
        """
        Verifica la conexión activa y carga las tablas desde la base de datos.
        """
        try:
            # Obtener la conexión activa
            connection = DatabaseConnection.get_connection()
            if not connection:
                raise RuntimeError("No hay una conexión activa con la base de datos.")
            
            self.all_tables = self.model.get_all_tables()  # Cargar todas las tablas

            # Poblar el combo box con las tablas cargadas
            self.view.populate_combo_box(self.all_tables)
            self.view.enable_table_controls(bool(self.all_tables))
        except Exception as e:
            print(f"Error al conectar y cargar las tablas: {e}")
            self.view.enable_table_controls(False)

    def filter_tables(self, text):
        """
        Filtra las tablas localmente según el texto ingresado.
        :param text: Texto ingresado para filtrar.
        """
        try:
            if not self.all_tables:
                print("La lista de tablas está vacía. Asegúrate de haber cargado las tablas.")
                return

            # Filtrar las tablas localmente
            filtered_tables = [table for table in self.all_tables if text.lower() in table.lower()]
            self.view.populate_combo_box(filtered_tables)
        except Exception as e:
            print(f"Error al filtrar las tablas: {e}")

    def ensure_connection_active(self):
        """
        Verifica si la conexión está activa, de lo contrario lanza un error controlado.
        """
        connection = DatabaseConnection.get_connection()
        if not connection:
            raise RuntimeError("No hay conexión activa con la base de datos. Asegúrese de establecer la conexión primero.")

    def get_table_structure(self, table_name):
        """
        Recupera la estructura de una tabla específica.
        :param table_name: Nombre de la tabla.
        :return: Estructura de la tabla como una lista de columnas y sus detalles.
        """
        try:
            self.ensure_connection_active()
            connection = DatabaseConnection.get_connection()
            return self.model.get_table_structure(table_name)
        except Exception as e:
            print(f"Error al obtener la estructura de la tabla {table_name}: {e}")
            return None

    def get_table_structure_for_validation(self, table_name):
        """
        Recupera la estructura de la tabla para validaciones específicas.
        :param table_name: Nombre de la tabla.
        :return: Estructura de la tabla.
        """
        try:
            self.ensure_connection_active()
            connection = DatabaseConnection.get_connection()
            return self.model.get_table_structure_for_validation(table_name)
        except Exception as e:
            print(f"Error al obtener la estructura para validación de la tabla {table_name}: {e}")
            return None

    def insert_data_to_table(self, table_name, dataframe, columns_to_insert, batch_size=1):
        """
        Inserta datos en la tabla seleccionada utilizando el modelo.
        :param table_name: Nombre de la tabla.
        :param dataframe: DataFrame con los datos a insertar.
        :param columns_to_insert: Columnas seleccionadas para la inserción.
        :param batch_size: Tamaño del lote para la inserción.
        :return: Resultado de la operación como un diccionario.
        """
        try:
            self.ensure_connection_active()
            connection = DatabaseConnection.get_connection()
            
            # Total de registros para la barra de progreso
            total_records = len(dataframe)

            # Inicializar ProgressDialog
            progress_dialog = ProgressDialog(total_records)
            progress_dialog.show()

            # Procesar la inserción a través del modelo
            result = {"success": [], "errors": []}
            for i in range(0, total_records, batch_size):
                batch = dataframe.iloc[i:i + batch_size]
                batch_result = self.model.insert_data(table_name, batch, columns_to_insert, batch_size)
                
                # Actualizar resultados acumulados
                result["success"].extend(batch_result["success"])
                result["errors"].extend(batch_result["errors"])
                
                # Actualizar barra de progreso
                progress_dialog.update_progress(len(result["success"]) + len(result["errors"]))
                QCoreApplication.processEvents()  # Permite refrescar la interfaz

            # Cerrar el diálogo al terminar
            progress_dialog.close_dialog()

            # Retornar el resumen de resultados
            return {
                "inserted": len(result["success"]),
                "errors": len(result["errors"]),
                "details": result["errors"]
            }

        except Exception as e:
            print(f"Error al insertar datos en la tabla {table_name}: {e}")
            return {
                "inserted": 0,
                "errors": len(dataframe),
                "details": [{"index": idx, "error": str(e)} for idx in dataframe.index]
            }

    def get_table_columns(self, table_name):
        """
        Obtiene las columnas de una tabla específica.
        :param table_name: Nombre de la tabla.
        :return: Lista de columnas de la tabla.
        """
        try:
            self.ensure_connection_active()
            connection = DatabaseConnection.get_connection()
            return self.model.get_table_columns(table_name)
        except Exception as e:
            print(f"Error al obtener las columnas de la tabla {table_name}: {e}")
            return []

    def insert_row(self, table_name, row_data):
        """
        Inserta una sola fila en la tabla especificada.
        :param table_name: Nombre de la tabla.
        :param row_data: Diccionario con los datos de la fila a insertar.
        :raises: Excepción si ocurre un error durante la inserción.
        """
        try:
            self.model.insert_row(table_name, row_data)
        except Exception as e:
            raise ValueError(f"Error al insertar fila en la tabla '{table_name}': {e}")

