import pandas as pd
from core.db_connection import DatabaseConnection

class TableModel:
    def __init__(self):
        """
        Inicializa el modelo de tabla.
        """
        pass

    def get_all_tables(self):
        """
        Recupera todas las tablas disponibles en la base de datos.
        :return: Lista de nombres de tablas.
        """
        connection = DatabaseConnection.get_connection()
        if not connection:
            raise ValueError("No hay conexión establecida.")

        query = "SELECT table_name FROM user_tables ORDER BY table_name"
        with connection.cursor() as cursor:
            cursor.execute(query)
            tables = [row[0] for row in cursor.fetchall()]
        return tables

    def get_table_structure(self, table_name):
        """
        Recupera la estructura de una tabla específica.
        :param table_name: Nombre de la tabla.
        :return: Estructura de la tabla como una lista de columnas y sus detalles.
        """
        connection = DatabaseConnection.get_connection()
        if not connection:
            raise ValueError("No hay conexión establecida.")

        query = f"""
            SELECT 
                column_name, 
                DATA_TYPE || 
                CASE 
                    WHEN DATA_TYPE = 'VARCHAR2' THEN 
                        ' (' || DATA_LENGTH || ' ' || 
                        CASE 
                            WHEN CHAR_USED = 'B' THEN 'Byte'
                            WHEN CHAR_USED = 'C' THEN 'Char'
                            ELSE 'Unknown' 
                        END || ')'
                    WHEN DATA_TYPE = 'NUMBER' THEN 
                        ' (' || DATA_PRECISION || 
                        CASE 
                            WHEN DATA_SCALE != 0 THEN ',' || DATA_SCALE 
                            ELSE '' 
                        END || ')'
                    ELSE ''
                END AS data_type, 
                CASE 
                    WHEN column_name IN (
                        SELECT column_name 
                        FROM user_cons_columns 
                        WHERE table_name = '{table_name}' 
                        AND constraint_name IN (
                            SELECT constraint_name 
                            FROM user_constraints 
                            WHERE constraint_type = 'P'
                        )
                    ) THEN 'Si' 
                    ELSE NULL 
                END AS is_pk,
                CASE 
                    WHEN nullable = 'Y' THEN NULL
                    ELSE 'No' 
                END AS allows_null,                
                (
                    SELECT COUNT(*) 
                    FROM USER_CONS_COLUMNS ucc
                    JOIN USER_CONSTRAINTS uc 
                    ON ucc.CONSTRAINT_NAME = uc.CONSTRAINT_NAME
                    AND ucc.OWNER = uc.OWNER
                    WHERE ucc.TABLE_NAME = '{table_name}'
                    AND ucc.COLUMN_NAME = utc.column_name
                    AND uc.CONSTRAINT_TYPE = 'C'
                ) AS "Constraints?",
                (
                    SELECT CASE 
                            WHEN COUNT(*) > 0 THEN 'Si'
                            ELSE NULL
                        END
                    FROM USER_CONS_COLUMNS ucc
                    JOIN USER_CONSTRAINTS uc 
                    ON ucc.CONSTRAINT_NAME = uc.CONSTRAINT_NAME
                    AND ucc.OWNER = uc.OWNER
                    WHERE ucc.TABLE_NAME = '{table_name}'
                    AND ucc.COLUMN_NAME = utc.column_name
                    AND uc.CONSTRAINT_TYPE = 'R'
                ) AS "Referencial?"
            FROM user_tab_columns utc
            WHERE table_name = '{table_name}'
            ORDER BY column_id
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            structure = cursor.fetchall()

        return [(col[0], col[1], col[2], col[3], col[4], col[5]) for col in structure]



    def insert_data(self, table_name, dataframe, columns_to_insert, batch_size=1):
        """
        Inserta datos en la tabla seleccionada.
        :param table_name: Nombre de la tabla.
        :param dataframe: DataFrame con los datos a insertar.
        :param columns_to_insert: Columnas seleccionadas para la inserción.
        :param batch_size: Tamaño del lote para la inserción (1 para fila por fila).
        :return: Diccionario con detalles de registros insertados y errores.
        """
        connection = DatabaseConnection.get_connection()
        if not connection:
            raise ValueError("No hay conexión establecida.")

        cursor = connection.cursor()
        success = []  # Índices de registros insertados correctamente
        errors = []   # Detalles de los errores: índice y mensaje

        # Construcción de la query de inserción
        columns_str = ", ".join([f'"{col}"' for col in columns_to_insert])
        values_str = ", ".join([f":{col}" for col in columns_to_insert])
        insert_query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str})"

        try:
            # Inserción por lotes o fila por fila
            for i in range(0, len(dataframe), batch_size):
                batch = dataframe.iloc[i:i + batch_size]
                data_list = []

                for index, row in batch.iterrows():
                    data_dict = {col: (row[col] if pd.notna(row[col]) else None) for col in columns_to_insert}
                    data_list.append(data_dict)

                try:
                    if batch_size > 1:
                        cursor.executemany(insert_query, data_list)  # Inserción por lotes
                    else:
                        cursor.execute(insert_query, data_list[0])  # Inserción fila por fila
                    success.extend(batch.index.tolist())
                except Exception as batch_error:
                    # Procesar errores de lote o fila
                    for index, row in batch.iterrows():
                        try:
                            data_dict = {col: (row[col] if pd.notna(row[col]) else None) for col in columns_to_insert}
                            cursor.execute(insert_query, data_dict)
                            success.append(index)
                        except Exception as row_error:
                            errors.append({"index": index, "error": str(row_error)})

            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()

        return {"success": success, "errors": errors}

    def get_table_columns(self, table_name):
        """
        Obtiene las columnas de una tabla específica.
        :param table_name: Nombre de la tabla.
        :return: Lista de columnas de la tabla en forma de diccionarios.
        """
        connection = DatabaseConnection.get_connection()
        if not connection:
            raise ValueError("No hay conexión establecida.")

        query = """
            SELECT column_name
            FROM user_tab_columns
            WHERE table_name = :table_name
        """
        with connection.cursor() as cursor:
            cursor.execute(query, {"table_name": table_name.upper()})
            # Retornar diccionarios con las columnas
            columns = [{"column_name": row[0]} for row in cursor.fetchall()]
        return columns

    def filter_tables(self, text):
        """
        Filtra las tablas que coincidan con el texto de búsqueda.
        :param text: Texto de búsqueda para filtrar tablas.
        :return: Lista de tablas filtradas.
        """
        all_tables = self.get_all_tables()
        return [table for table in all_tables if text.lower() in table.lower()]
    
    def get_table_structure_for_validation(self, table_name):
        """
        Recupera la estructura de una tabla para validación.
        :param table_name: Nombre de la tabla.
        :return: Lista de columnas con detalles relevantes para la validación.
        """
        connection = DatabaseConnection.get_connection()
        if not connection:
            raise ValueError("No hay conexión establecida.")

        query = f"""
        SELECT utc.COLUMN_NAME AS column_name,
               utc.DATA_TYPE || 
               CASE 
                   WHEN utc.DATA_TYPE = 'VARCHAR2' THEN 
                       ' (' || utc.CHAR_LENGTH || ' ' || 
                       CASE 
                           WHEN utc.CHAR_USED = 'B' THEN 'Byte'
                           WHEN utc.CHAR_USED = 'C' THEN 'Char'
                           ELSE 'Unknown' 
                       END || ')'
                   WHEN utc.DATA_TYPE = 'NUMBER' THEN 
                       ' (' || utc.DATA_PRECISION || 
                       CASE 
                           WHEN utc.DATA_SCALE != 0 THEN ',' || utc.DATA_SCALE 
                           ELSE '' 
                       END || ')'
                   ELSE ''
               END AS data_type_formatted,
               utc.DATA_TYPE,
               utc.COLUMN_ID,
               utc.DATA_PRECISION,
               utc.CHAR_LENGTH AS DATA_LENGTH,
               utc.DATA_SCALE
        FROM USER_TAB_COLUMNS utc
        WHERE utc.TABLE_NAME = :table_name
        ORDER BY utc.COLUMN_ID
        """
        
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, {"table_name": table_name})
                structure = cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener la estructura de la tabla {table_name}: {e}")
            return []

        # Procesar los datos obtenidos
        columns = []
        for col in structure:
            column_name = col[0]
            data_type_formatted = col[1]
            data_type = col[2]
            column_id = col[3]
            precision = col[4] if col[4] else None
            length = col[5] if col[5] else None
            scale = col[6] if col[6] else None

            # Construir el diccionario con la información relevante
            column_info = {
                'column_name': column_name,
                'data_type': data_type,
                'data_type_formatted': data_type_formatted,
                'precision': precision,
                'length': length,
                'scale': scale,
            }
            columns.append(column_info)

        return columns

    def insert_row(self, table_name, row_data):
        """
        Inserta una sola fila en la tabla especificada.
        :param table_name: Nombre de la tabla.
        :param row_data: Diccionario con los datos de la fila.
        :raises: Excepción si ocurre un error durante la inserción.
        """
        connection = DatabaseConnection.get_connection()
        if not connection:
            raise ValueError("No hay conexión establecida.")

        cursor = connection.cursor()
        columns_str = ", ".join([f'"{col}"' for col in row_data.keys()])
        values_str = ", ".join([f":{col}" for col in row_data.keys()])
        insert_query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str})"

        try:
            cursor.execute(insert_query, row_data)
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise ValueError(f"Error al insertar fila: {e}")
        finally:
            cursor.close()
