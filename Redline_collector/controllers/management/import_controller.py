class ImportController:
    def __init__(self, table_controller, dataframe):
        """
        Inicializa el controlador de importación.
        :param table_controller: Instancia de TableController con conexión activa.
        :param dataframe: DataFrame con los datos cargados del archivo.
        """
        self.table_controller = table_controller
        self.dataframe = dataframe
        self.is_cancelled = False
        # Verificar que la conexión esté activa antes de continuar
        self.table_controller.ensure_connection_active()

    def cancel(self):
        """
        Cancela el proceso de importación estableciendo el flag `is_cancelled`.
        """
        self.is_cancelled = True

    def import_data(self, table_name, columns_to_insert, on_omitted_callback=None, progress_callback=None):
        """
        Controla el proceso de importación de los datos desde el dataframe a la base de datos.
        Procesa los registros uno a uno para manejar los errores en tiempo real.
        :param table_name: Nombre de la tabla en la base de datos.
        :param columns_to_insert: Lista de las columnas que serán insertadas en la tabla.
        :param on_omitted_callback: Función que será llamada cuando un registro sea omitido.
        :param progress_callback: Función que será llamada para actualizar el progreso.
        :return: Resumen del proceso de importación.
        """
        if self.dataframe.empty:
            raise ValueError("El DataFrame está vacío. No hay datos para importar.")

        omitted_records = []  # Registros omitidos con detalles de errores
        inserted_count = 0    # Contador de registros insertados correctamente
        total_records = len(self.dataframe)

        for idx, row in self.dataframe.iterrows():
            if self.is_cancelled:
                # Detener el proceso si el usuario lo cancela
                break

            try:
                # Extraer solo las columnas relevantes para la inserción
                row_data = {col: row[col] for col in columns_to_insert if col in row}

                # Intentar insertar la fila en la base de datos usando el controlador de tablas
                self.table_controller.insert_row(table_name, row_data)
                inserted_count += 1
            except Exception as e:
                # En caso de error, agregar el registro omitido y su error
                omitted_record = row.to_dict()
                omitted_record["Errores"] = str(e)
                omitted_records.append(omitted_record)

                # Llamar al callback para notificar a la vista
                if on_omitted_callback:
                    on_omitted_callback(omitted_record)

            # Llamar al callback para actualizar el progreso
            if progress_callback:
                progress_callback(inserted_count + len(omitted_records), total_records)

        # Retornar un resumen del proceso
        return {
            "inserted": inserted_count,
            "errors": len(omitted_records),
            "details": omitted_records,
            "cancelled": self.is_cancelled
        }

    def validate_columns(self, visible_columns, table_name):
        """
        Valida las columnas visibles que coinciden entre la tabla y el dataframe.
        :param visible_columns: Lista de diccionarios con nombre y datos únicos de las columnas coincidentes.
        :param table_name: Nombre de la tabla.
        :return: Lista con los resultados de validación por columna, incluyendo las filas con errores.
        """
        validation_results = []
        table_structure = self.table_controller.get_table_structure_for_validation(table_name)

        for column in table_structure:
            column_name = column["column_name"]
            column_type = column["data_type"]
            precision = column.get("precision")
            scale = column.get("scale")
            length = column.get("length")

            column_data = next(
                (col["data"] for col in visible_columns if col["column_name"] == column_name),
                None
            )

            if column_data is not None:
                if column_type == "NUMBER":
                    error, error_rows = self.validate_number_column(column_data, precision, scale)
                elif column_type == "VARCHAR2":
                    error, error_rows = self.validate_varchar_column(column_data, length)
                else:
                    error = f"Tipo de dato {column_type} no soportado."
                    error_rows = []

                validation_results.append({
                    "column_name": column_name,
                    "status": "Correcto" if not error_rows else "Incorrecto",
                    "errores": ', '.join(map(str, error_rows)) if error_rows else "Ningún error"
                })
            else:
                validation_results.append({
                    "column_name": column_name,
                    "status": "No disponible en el dataframe",
                    "errores": "Ningún error"
                })

        return validation_results

    def get_table_columns(self, table_name):
        """
        Obtiene las columnas de la tabla desde el controlador de tabla.
        :param table_name: Nombre de la tabla.
        :return: Lista de columnas de la tabla.
        """
        return self.table_controller.get_table_columns(table_name)

    def load_table_structure(self, table_name):
        """
        Método para cargar la estructura de la tabla usando el controlador de la tabla.
        """
        columns = self.table_controller.get_table_structure_for_validation(table_name)
        return columns

    def validate_number_column(self, column_data, precision, scale):
        """
        Valida una columna de tipo NUMBER, considerando precisión y escala.
        """
        scale = scale or 0
        error_rows = []

        for idx, value in enumerate(column_data):
            try:
                if isinstance(value, (int, float)):
                    if scale > 0 and '.' in str(value) and len(str(value).split('.')[1]) > scale:
                        error_rows.append(idx + 1)
                    if precision is not None and len(str(int(abs(value)))) > precision:
                        error_rows.append(idx + 1)
                else:
                    float_value = float(value)
                    if precision is not None and len(str(int(abs(float_value)))) > precision:
                        error_rows.append(idx + 1)
            except (ValueError, TypeError):
                error_rows.append(idx + 1)

        return None, error_rows

    def validate_varchar_column(self, column_data, length):
        """
        Valida una columna de tipo VARCHAR2 según su longitud máxima permitida.
        """
        error_rows = []

        for idx, value in enumerate(column_data):
            if len(str(value)) > length:
                error_rows.append(idx + 1)

        return None, error_rows
