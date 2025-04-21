from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar, QPushButton
from PyQt5.QtCore import pyqtSignal, Qt

class ProgressDialog(QDialog):
    cancel_signal = pyqtSignal()  # Señal para cancelar el proceso

    def __init__(self, total_records, parent=None):
        super().__init__(parent)
        self.total_records = total_records
        self.setWindowTitle("Progreso de Importación")
        self.setFixedSize(400, 150)
        self.message_template = "Registros procesados: {processed} de {total}"

        layout = QVBoxLayout()
        self.label = QLabel(self.message_template.format(processed=0, total=self.total_records))
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(self.total_records)
        self.cancel_button = QPushButton("Cancelar")

        self.cancel_button.clicked.connect(self.emit_cancel_signal)

        layout.addWidget(self.label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.cancel_button)
        self.setLayout(layout)

    def update_progress(self, processed_records):
        """
        Actualiza el progreso en la barra y la etiqueta.
        """
        self.label.setText(self.message_template.format(processed=processed_records, total=self.total_records))
        self.progress_bar.setValue(processed_records)

    def emit_cancel_signal(self):
        """
        Emite la señal de cancelación cuando se presiona el botón "Cancelar".
        """
        self.cancel_signal.emit()
        self.close()

    def close_dialog(self):
        """
        Cierra el diálogo manualmente.
        """
        self.close()
