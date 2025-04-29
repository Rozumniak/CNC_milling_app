# logic/milling_calculator.py

from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QMessageBox
from logic.query_db import get_feed_A1, get_feed_A2

class MillingCalculator:
    def __init__(self, window):
        self.window = window
        self.connect_signals()

    def connect_signals(self):
        self.window.calculate_button.clicked.connect(self.clear_all_errors)
        self.window.calculate_button.clicked.connect(self.tool_diameter_check)
        self.window.calculate_button.clicked.connect(self.depth_calculation)
        self.window.calculate_button.clicked.connect(self.feed_calculation)

        self.window.milling_width_input.textEdited.connect(lambda: self.clear_error(self.window.milling_width_input))
        self.window.tool_diameter_input.textEdited.connect(lambda: self.clear_error(self.window.tool_diameter_input))
        self.window.milling_depth_input.textEdited.connect(lambda: self.clear_error(self.window.milling_depth_input))
        self.window.length_input.textEdited.connect(lambda: self.clear_error(self.window.length_input))
        self.window.width_input.textEdited.connect(lambda: self.clear_error(self.window.width_input))
        self.window.height_input.textEdited.connect(lambda: self.clear_error(self.window.height_input))
        self.window.teeth_number_input.textEdited.connect(lambda: self.clear_error(self.window.teeth_number_input))

    def tool_diameter_check(self):

        error_fields = []

        milling_width_text = self.window.milling_width_input.text().strip()
        tool_diameter_text = self.window.tool_diameter_input.text().strip()

        if not tool_diameter_text:
            error_fields.append(self.window.tool_diameter_input)
        if not milling_width_text:
            error_fields.append(self.window.milling_width_input)

        if error_fields:
            self.set_input_errors(error_fields)
            self.show_error_popup("Поле 'Діаметр фрези' або 'Ширина фрезерування' пусте!")
            return

        try:
            milling_width = float(milling_width_text)
            tool_diameter = float(tool_diameter_text)
        except ValueError:
            self.set_input_errors([self.window.milling_width_input, self.window.tool_diameter_input])
            self.show_error_popup("Некоректні числові значення в полях 'Діаметр фрези' або 'Ширина фрезерування'.")
            return

        tool_type = self.window.tool_type_combo.currentText()

        if tool_type == "Торцева":
            if milling_width >= tool_diameter:
                self.set_input_errors([self.window.milling_width_input, self.window.tool_diameter_input])
                self.show_error_popup("При торцевому фрезеруванні ширина фрезерування повинна бути меншою за діаметр фрези.")
                return
        else:
            if milling_width < tool_diameter:
                self.set_input_errors([self.window.milling_width_input, self.window.tool_diameter_input])
                self.show_error_popup("Для даного типу фрези ширина фрезерування має бути більшою за діаметр.")
                return

    def depth_calculation(self):

        error_fields = []

        milling_depth_text = self.window.milling_depth_input.text().strip()

        if not milling_depth_text:
            error_fields.append(self.window.milling_depth_input)

        if error_fields:
            self.set_input_errors(error_fields)
            self.window.result_depth.setText("-")  # Очищення результату при помилці
            self.show_error_popup("Поле 'Припуск на обробку' пусте!")
            return

        try:
            milling_depth = float(milling_depth_text)
        except ValueError:
            self.set_input_errors([self.window.milling_depth_input])
            self.window.result_depth.setText("-")  # Очищення результату при помилці
            self.show_error_popup("Некоректне значення в полі 'Припуск на обробку'.")
            return

        processing_type = self.window.processing_type_combo.currentText()

        if processing_type == "Чорнова":
            if milling_depth < 5:
                self.window.result_depth.setText(str(milling_depth))
            else:
                self.window.result_depth.setText("2.5")
        elif processing_type == "Напівчистова":
            self.window.result_depth.setText("1.5")
        elif processing_type == "Чистова":
            self.window.result_depth.setText("1.0")


    def feed_calculation(self):
        processing_type = self.window.processing_type_combo.currentText()
        tool_type = self.window.tool_type_combo.currentText()
        tool_material = self.window.tool_material_combo.currentText()
        material = self.window.material_combo.currentText()
        workbench_power_less = self.window.workbench_power_less.isChecked()
        workbench_power_mid = self.window.workbench_power_mid.isChecked()
        workbench_power_more = self.window.workbench_power_more.isChecked()
        tooth_size_large = self.window.tooth_size_large.isChecked()
        tooth_size_small = self.window.tooth_size_small.isChecked()

        if (processing_type == "Чорнова"
            and tool_material == "Твердий сплав"
            and tool_type in ["Торцева", "Циліндрична", "Дискова"]):

            if workbench_power_less or workbench_power_mid:
                x = "<10"
                feed = get_feed_A1(material, x)
                self.window.result_feed_rate.setText(str(feed))
            elif workbench_power_more:
                x = ">10"
                feed = get_feed_A1(material, x)
                self.window.result_feed_rate.setText(str(feed))

        if (processing_type == "Чорнова"
            and tool_material == "Швидкорізальна сталь"
            and tool_type in ["Торцева", "Циліндрична", "Дискова"]):

            feed = get_feed_A2(material, workbench_power_less, workbench_power_mid, workbench_power_more, tooth_size_large, tooth_size_small, tool_type)
            self.window.result_feed_rate.setText(str(feed))



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
            self.window.milling_depth_input,
            self.window.length_input,
            self.window.width_input,
            self.window.height_input
        ]
        for widget in fields:
            palette = widget.palette()
            palette.setColor(QPalette.Base, QColor('#ffffff'))
            widget.setStyleSheet("")
            widget.setPalette(palette)

    def clear_error(self, widget):
        palette = widget.palette()
        palette.setColor(QPalette.Base, QColor('#ffffff'))  # Змінюємо фон назад на білий
        widget.setStyleSheet("")
        widget.setPalette(palette)

    def show_error_popup(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Помилка")
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()