from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
from views.main_view import MainView  # Vista principal actual
from utils.ui_styles import apply_style
import os
import sys

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("REDLINE Collector")
        self.setGeometry(0, 0, 800, 600)
        self.set_window_icon()

        # Configurar solo la vista principal
        self.main_view = MainView()
        self.setCentralWidget(self.main_view)

        # Maximizar la ventana al iniciar
        self.showMaximized()

        # Aplicar el estilo y centrar ventana si es necesario
        self.set_app_style()

    def set_window_icon(self):
        # Obtener el directorio base según el entorno (normal o ejecutable empaquetado)
        base_path = os.path.dirname(os.path.abspath(sys.executable)) if getattr(sys, 'frozen', False) else os.path.abspath(".")
        icon_file = os.path.join(base_path, 'styles', 'SDS.ico')
        self.setWindowIcon(QIcon(icon_file))

    def set_app_style(self):
        # Aplicar estilo predefinido desde ui_styles.py
        apply_style(self, "main_window")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Configurar el ícono de la aplicación
    icon_path = os.path.join(os.path.dirname(__file__), "styles", "SDS.ico")
    app.setWindowIcon(QIcon(icon_path))

    # Crear y mostrar la ventana principal
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
