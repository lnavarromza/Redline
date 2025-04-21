from PyQt5.QtWidgets import QApplication

def center_window(window):
    """Centra la ventana en la pantalla."""
    screen_geometry = QApplication.desktop().screenGeometry(window)
    window_geometry = window.frameGeometry()
    center_point = screen_geometry.center()
    window_geometry.moveCenter(center_point)
    window_geometry.moveTop(window_geometry.top() - 30)
    window.move(window_geometry.topLeft())

# Estilos CSS predefinidos
STYLES = {
    "main_window": """QMainWindow {
            background-color: #ffffff; /* Fondo blanco */
        }
        QWidget {
            background-color: #ffffff;
            color: #333333;
            font-family: Arial, sans-serif;
            font-size: 14px;
        }
        QLabel {
            color: #333333;
            font-size: 14px;
            font-weight: normal;
            margin-bottom: 8px;
        } 
        QPushButton {
            background-color: #d32f2f; /* Rojo para el botón principal */
            color: #ffffff;
            border: none;
            border-radius: 4px;
            padding: 12px 18px;
            font-size: 14px;
            min-width: 120px; /* Tamaño mínimo para botones */
            max-width: 200px; /* Tamaño máximo */
        }
        QPushButton:hover {
            background-color: #b71c1c; /* Hover más oscuro */
        }
        QLineEdit {
            border: 1px solid #dcdcdc;
            border-radius: 4px;
            padding: 8px;
            font-size: 14px;
            background-color: #ffffff;
            min-height: 30px;
        }
        QLineEdit:focus {
            border: 1px solid #a6a6a6;
        }
        QCheckBox {
            font-size: 14px;
            color: #555555;
        }
        QLabel#help_label {
            font-size: 14px;
            color: #007bff; /* Azul para la etiqueta de ayuda */
            text-decoration: underline;
        }
        QLabel#help_label:hover {
            color: #0056b3;
        }
        QTableView {
            background-color: #ffffff; /* Fondo blanco para la tabla */
            border: 1px solid #cccccc; /* Borde gris claro */
            gridline-color: #dddddd;   /* Líneas divisoras */
            font-size: 14px;
        }
        QTableView::item {
            background-color: #ffffff; /* Fondo blanco de las celdas */
            color: #333333;            /* Texto oscuro */
            border: none;              /* Sin bordes adicionales */
            padding: 6px;              /* Espaciado interno */
        }
        QTableView::item:selected {
            background-color: #e0e0e0; /* Fondo gris claro para la celda seleccionada */
            color: #333333;            /* Texto oscuro */
        }
        QTableView QHeaderView::section {
            background-color: #f5f5f5; /* Fondo gris claro para la cabecera */
            color: #007acc;            /* Texto azul */
            font-weight: bold;         /* Texto en negrita */
            padding: 8px;              /* Espaciado interno */
            border: 1px solid #cccccc; /* Borde gris claro */
            text-align: left;          /* Alineación del texto a la izquierda */
        }
        QTableView QHeaderView {
            border: none;              /* Sin bordes adicionales */
        }
        QComboBox {
            background-color: #ffffff; /* Fondo blanco */
            border: 1px solid #cccccc; /* Borde gris claro */
            border-radius: 4px;        /* Esquinas redondeadas */
            padding: 8px;             /* Espaciado interno */
            color: #333333;           /* Texto oscuro */
            font-size: 14px;          /* Tamaño de fuente */
        }
        QComboBox:hover {
            border: 1px solid #888888; /* Borde más oscuro al pasar el mouse */
        }
        QComboBox::drop-down {
            border: none;             /* Sin borde adicional */
            background: #f5f5f5;      /* Fondo gris claro */
            border-left: 1px solid #cccccc; /* Borde separador de la flecha */
            width: 30px;              /* Ancho del área del ícono */
        }
        QComboBox::down-arrow {
            image: url(down_arrow.png); /* Ícono personalizado (debes agregar el archivo en tu proyecto) */
            width: 10px;
            height: 10px;
        }
        QComboBox::down-arrow:hover {
            image: url(down_arrow_hover.png); /* Cambia el ícono cuando se pase el mouse (opcional) */
        }
    """,
    "dark_mode": """QWidget {
            background-color: #2e2e2e;
            color: #ffffff;
            font-family: Helvetica, sans-serif;
        }
        QPushButton {
            background-color: #505050;
            color: white;
            border: none;
            padding: 8px 12px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #606060;
        }
    """,
    "table_widget_style": """
            QTableWidget {
                background-color: #ffffff; /* Fondo blanco para la tabla */
                border: 1px solid #cccccc; /* Borde gris claro */
                gridline-color: #dddddd;   /* Líneas divisoras */
                font-size: 14px;
            }
            QTableWidget::item {
                background-color: #ffffff; /* Fondo blanco de las celdas */
                color: #333333;            /* Texto oscuro */
                border: none;              /* Sin bordes adicionales */
                padding: 6px;              /* Espaciado interno */
            }
            QTableWidget::item:selected {
                background-color: #e0e0e0; /* Fondo gris claro para la celda seleccionada */
                color: #333333;            /* Texto oscuro */
            }
            QTableWidget QHeaderView::section {
                background-color: #f5f5f5; /* Fondo gris claro para la cabecera */
                color: #007acc;            /* Texto azul */
                font-weight: bold;         /* Texto en negrita */
                padding: 8px;              /* Espaciado interno */
                border: 1px solid #cccccc; /* Borde gris claro */
                text-align: left;          /* Alineación del texto a la izquierda */
            }
            QTableWidget QHeaderView {
                border: none;              /* Sin bordes adicionales */
            }
        """,
    "file_block": """QFrame {
            border: 1px solid #dcdcdc;
            border-radius: 4px;
            margin: 5px;
            padding: 10px;
        }
        QLabel {
            font-size: 14px;
            font-weight: bold;
            margin-bottom: 10px;
        }
    """,
    "title_label": """QLabel {
            color: #d32f2f;  /* Rojo oscuro */
            font-size: 24px; /* Tamaño de fuente */
            font-weight: bold; /* Texto en negrita */
            border: 2px solid #d32f2f; /* Borde del mismo color que el texto */
            border-radius: 8px; /* Esquinas redondeadas */
            padding: 10px 20px; /* Espaciado interno */
            background-color: #fff5f5; /* Fondo rojo claro */
            margin: 20px 0px; /* Espaciado vertical */
            text-align: center; /* Centrado del texto */
        }
    """,
    "popup_window": """QWidget {
            background-color: #ffffff;
            border: 1px solid #ccc;
            font-family: Arial;
            font-size: 14px;
        }
    """,
    "search_container_style": """
            QWidget {
                background-color: #ffffff; /* Fondo blanco */
                padding: 5px;              /* Espaciado interno */
                border: none;              /* Eliminar borde innecesario */
                border-radius: 4px;        /* Esquinas redondeadas */
            }
            QLabel {
                color: #333333;
                font-size: 14px;
                font-weight: normal;
                margin-right: 10px;
            }
            QLineEdit {
                border: 1px solid #dcdcdc;
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
                background-color: #ffffff;
                min-height: 30px;
                margin-bottom: 10px; /* Agregar espacio adicional */
            }
            QLineEdit:focus {
                border: 1px solid #a6a6a6;
            }
        """

}

def apply_style(widget, style_name):
    """Aplica un estilo predefinido a un widget."""
    style = STYLES.get(style_name)
    if style:
        widget.setStyleSheet(style)
    else:
        raise ValueError(f"Estilo '{style_name}' no encontrado en STYLES.")