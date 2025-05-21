# logic/milling_calculator.py

from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QMessageBox
from logic.query_db import get_feed_A1, get_feed_A2, get_feed_A3, get_feed_A4, get_feed_A5, get_cutting_speeds_A6, get_tool_life_A8, get_Knv, get_Kuv, get_cutting_speeds_A7, get_nv, get_machines


class MillingCalculator:
    def __init__(self, window):
        self.window = window
        self.connect_signals()

    def connect_signals(self):
        self.window.calculate_button.clicked.connect(self.clear_result)
        self.window.calculate_button.clicked.connect(self.clear_all_errors)
        self.window.calculate_button.clicked.connect(self.tool_diameter_check)
        self.window.calculate_button.clicked.connect(self.depth_calculation)
        self.window.calculate_button.clicked.connect(self.feed_calculation)
        self.window.calculate_button.clicked.connect(self.speed_calculation)
        self.window.calculate_button.clicked.connect(self.get_suitable_machines)


        self.window.milling_width_input.textEdited.connect(lambda: self.clear_error(self.window.milling_width_input))
        self.window.tool_diameter_input.textEdited.connect(lambda: self.clear_error(self.window.tool_diameter_input))
        self.window.milling_depth_input.textEdited.connect(lambda: self.clear_error(self.window.milling_depth_input))
        """self.window.length_input.textEdited.connect(lambda: self.clear_error(self.window.length_input))
        self.window.width_input.textEdited.connect(lambda: self.clear_error(self.window.width_input))
        self.window.height_input.textEdited.connect(lambda: self.clear_error(self.window.height_input))"""
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
        tool_diameter = self.window.tool_diameter_input.text()
        material = self.window.material_combo.currentText()
        workbench_power_less = self.window.workbench_power_less.isChecked()
        workbench_power_mid = self.window.workbench_power_mid.isChecked()
        workbench_power_more = self.window.workbench_power_more.isChecked()
        tooth_size_large = self.window.tooth_size_large.isChecked()
        tooth_size_small = self.window.tooth_size_small.isChecked()
        cutting_element = self.window.tool_subtype_2_combo.currentText()
        depth = float(self.window.result_depth.text())

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

        elif (processing_type == "Чорнова"
            and tool_material == "Швидкорізальна сталь"
            and tool_type in ["Торцева", "Циліндрична", "Дискова"]):

            feed = get_feed_A2(material, workbench_power_less, workbench_power_mid, workbench_power_more, tooth_size_large, tooth_size_small, tool_type)
            self.window.result_feed_rate.setText(str(feed))

        elif (processing_type == "Чистова"
            and tool_material in ["Швидкорізальна сталь", "Твердий сплав"]
            and tool_type in ["Торцева", "Циліндрична", "Дискова"]):

            feed = get_feed_A3(material, tool_type, tool_diameter, tool_material)
            self.window.result_feed_rate.setText(str(feed))

        elif (processing_type == "Чорнова"
            and tool_type == "Кінцева"):

            cutting_element_map = {
                "З коронками": "Коронка",
                "Цілісна": "Коронка",
                "З напаяними пластинами": "Гвинтові пластинки"
            }

            if cutting_element in cutting_element_map:
                cutting_element = cutting_element_map[cutting_element]
            else:
                return None

            feed = get_feed_A4(cutting_element, tool_diameter, depth)
            self.window.result_feed_rate.setText(str(feed))

        elif (processing_type == "Чистова"
            and tool_type == "Кінцева"):
            feed = get_feed_A5(tool_diameter)
            self.window.result_feed_rate.setText(str(feed))

    def speed_calculation(self):
        material_A6_list = [
            "Сталь конструкційна Т5К12В", "Сталь конструкційна Т5К10", "Сталь конструкційна P18",
            "Сталь конструкційна Т15К6", "Сталь конструкційна Р6М5", "Сталь конструкційна Т30К4",
            "Сталь конструкційна ВК8", "Сталь загартована Т15К6 HRC 35-50", "Сталь загартована Т30К4 HRC 35-50",
            "Сталь загартована ВК6 HRC 35-50", "Сталь загартована ВК8 HRC 35-50",
            "Сталь загартована ВК4 HRC 51-62", "Сталь загартована ВК6 HRC 51-62", "Сталь загартована ВК8 HRC 51-62",
            "Чавун ВК8 HRC 35-50", "Чавун ВК6 HRC 35-50", "Чавун ВК4 HRC 35-50",
            "Чавун ВК3 HRC 35-50", "Чавун Р18 HRC 51-62", "Чавун Р6М3 HRC 51-62",
        ]
        material_A7_list = [
            "Мідь Р6М5 HRC 35-50", "Мідь ВК4 HRC 35-50",
            "Мідь ВК6 HRC 35-50", "Мідь 9ХС HRC 35-50",
            "Мідь ХВГ HRC 51-62", "Мідь У12А HRC 51-62",
            "Алюміній Р6М5 HRC 35-50", "Алюміній ВК4 HRC 35-50",
            "Алюміній ВК6 HRC 35-50", "Алюміній 9ХС HRC 35-50",
            "Алюміній ХВГ HRC 51-62", "Алюміній У12А HRC 51-62",
        ]

        material_category_map = {
            "Сталь конструкційна Т5К12В": "Сталь",
            "Сталь конструкційна Т5К10": "Сталь",
            "Сталь конструкційна P18": "Сталь",
            "Сталь конструкційна Т15К6": "Сталь",
            "Сталь конструкційна Р6М5": "Сталь",
            "Сталь конструкційна Т30К4": "Сталь",
            "Сталь конструкційна ВК8": "Сталь",
            "Сталь загартована Т15К6 HRC 35-50": "Сталь",
            "Сталь загартована Т30К4 HRC 35-50": "Сталь",
            "Сталь загартована ВК6 HRC 35-50": "Сталь",
            "Сталь загартована ВК8 HRC 35-50": "Сталь",
            "Сталь загартована ВК4 HRC 51-62": "Сталь",
            "Сталь загартована ВК6 HRC 51-62": "Сталь",
            "Сталь загартована ВК8 HRC 51-62": "Сталь",

            "Чавун ВК8 HRC 35-50": "Чавун",
            "Чавун ВК6 HRC 35-50": "Чавун",
            "Чавун ВК4 HRC 35-50": "Чавун",
            "Чавун ВК3 HRC 35-50": "Чавун",
            "Чавун Р18 HRC 51-62": "Чавун",
            "Чавун Р6М3 HRC 51-62": "Чавун",

            "Мідь Р6М5 HRC 35-50" : "Мідь",
            "Мідь ВК4 HRC 35-50" : "Мідь",
            "Мідь ВК6 HRC 35-50" : "Мідь",
            "Мідь 9ХС HRC 35-50" : "Мідь",
            "Мідь ХВГ HRC 51-62" : "Мідь",
            "Мідь У12А HRC 51-62" : "Мідь",
            "Алюміній Р6М5 HRC 35-50" : "Алюміній",
            "Алюміній ВК4 HRC 35-50" : "Алюміній",
            "Алюміній ВК6 HRC 35-50" : "Алюміній",
            "Алюміній 9ХС HRC 35-50" : "Алюміній",
            "Алюміній ХВГ HRC 51-62" : "Алюміній",
            "Алюміній У12А HRC 51-62" : "Алюміній",
        }
        material = self.window.material_combo.currentText()
        if material in material_category_map:
            material_category = material_category_map[material]
        else:
            return None

        tool_type = self.window.tool_type_combo.currentText()
        tool_material = self.window.tool_material_combo.currentText()
        milling_width = float(self.window.milling_width_input.text())
        depth = float(self.window.result_depth.text())
        feed = float(self.window.result_feed_rate.text())
        tool_diameter = self.window.tool_diameter_input.text()
        teeth_number = float(self.window.teeth_number_input.text())
        surface_state = self.window.surface_state_combo.currentText()

        if (tool_type == "Дискова"):
            tool_subtype = self.window.tool_subtype_1_combo.currentText()
        elif (tool_type == "Кінцева"):
            tool_subtype = self.window.tool_subtype_2_combo.currentText()

        if (tool_type == "Торцева"):
            tool_subtype = None
        if (tool_type == "Циліндрична"):
            tool_subtype = None

        if (material in material_A6_list):
            material_strength = float(self.window.material_strength_input.text())
            power = get_cutting_speeds_A6(material, material_strength, tool_type, tool_subtype, tool_material,
                                          milling_width, depth, feed)

        if (material in material_A7_list):
            power = get_cutting_speeds_A7(material, tool_type, feed)


        if power is not None:
            Cv = power[0]
            q = power[1]
            m = power[2]
            x = power[3]
            y = power[4]
            u = power[5]
            p = power[6]

        Knv = get_Knv(surface_state)
        Kuv = get_Kuv(material)
        nv = float(get_nv(material, tool_material))

        if (material_category == "Сталь"):
            material_strength = float(self.window.material_strength_input.text())
            Kmv = (750 / material_strength) ** nv
        elif (material_category == "Чавун"):
            material_strength = float(self.window.material_strength_input.text())
            Kmv = (1900 / material_strength) ** nv
        elif (material_category == "Мідь"):
            Kmv = 1.8
        elif (material_category == "Алюміній"):
            Kmv = 1
        Kv = Knv * Kuv * Kmv

        tool_life = get_tool_life_A8(tool_type, tool_diameter)

        Vp = ((Cv * (float(tool_diameter) ** q)) / ((tool_life ** m) * (depth ** x) * (feed ** y) * (milling_width ** u) * (teeth_number ** p))) * Kv

        self.window.result_cutting_speed.setText(str(round(Vp, 2)))

        np = (1000 * Vp) / (3.14 * float(tool_diameter))

        self.window.result_spindle_speed.setText(str(round(np, 0)))

    def get_suitable_machines(self):
        teeth_number = float(self.window.teeth_number_input.text())
        processing_type = self.window.processing_type_combo.currentText()
        spindle_speed = float(self.window.result_spindle_speed.text())
        feed = float(self.window.result_feed_rate.text())

        if (processing_type == "Чорнова"):
            minute_feed = feed * spindle_speed * teeth_number
        else :
            minute_feed = feed * spindle_speed

        machines = get_machines(minute_feed, spindle_speed)
        result_text = ""
        for machine in machines:
            result_text += f"Модель: {machine[0]}, Тип: {machine[1]}, Розмір столу: {machine[2]}\n"
            self.window.machines.setText(result_text)
            print(f"Модель: {machine[0]}, Тип: {machine[1]}, Розмір столу: {machine[2]}")

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
            self.window.milling_depth_input
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

    def clear_result(self):
        self.window.result_depth.setText("-")
        self.window.result_feed_rate.setText("-")
        self.window.result_cutting_speed.setText("-")
        self.window.result_spindle_speed.setText("-")