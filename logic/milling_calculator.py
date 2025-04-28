# logic/milling_calculator.py

from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QMessageBox
class MillingCalculator:
    def __init__(self, window):
        self.window = window
        self.connect_signals()

    def connect_signals(self):
        self.window.calculate_button.clicked.connect(self.tool_diameter_check)

    def on_calculate_clicked(self):
        pass

    def tool_diameter_check(self):
        try:
            milling_width = float(self.window.milling_width_input.text())
            tool_diameter = float(self.window.tool_diameter_input.text())
            tool_type = self.window.tool_type_combo.currentText()
        except ValueError:
            milling_width = 0  # Якщо введено не число
            tool_diameter = 0

        error_fields = []

        if not self.window.tool_diameter_input.text().strip():
            print("Поле порожнє")
        else:
            if tool_type == "Торцева":
                if milling_width >= tool_diameter:
                    error_fields.append(self.window.milling_width_input)
                    error_fields.append(self.window.tool_diameter_input)
            else:
                if milling_width < tool_diameter:
                    error_fields.append(self.window.milling_width_input)
                    error_fields.append(self.window.tool_diameter_input)

            # Спочатку знімаємо підсвічування з усіх полів
        self.clear_all_errors()

        if error_fields:
            self.set_input_errors(error_fields)
            self.show_error_popup(
                "При торцевому фрезеруванні діаметр фрези повинен бути більше за ширину фрезерування.")

    def set_input_errors(self, input_widgets):
        for widget in input_widgets:
            palette = widget.palette()
            palette.setColor(QPalette.Base, QColor('#ffcccc'))
            widget.setStyleSheet("border: 2px solid red;")
            widget.setPalette(palette)

    def clear_all_errors(self):
        # Повертаємо стандартний вигляд для всіх полів, які потрібно перевіряти
        fields = [
            self.window.milling_width_input,
            self.window.tool_diameter_input,
            self.window.length_input,
            self.window.width_input,
            self.window.height_input
        ]
        for widget in fields:
            palette = widget.palette()
            palette.setColor(QPalette.Base, QColor('#ffffff'))
            widget.setStyleSheet("")
            widget.setPalette(palette)

    def show_error_popup(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Помилка")
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()
