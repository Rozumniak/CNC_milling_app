# gui/main_window.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QLineEdit,
    QFormLayout, QGroupBox, QRadioButton, QButtonGroup, QHBoxLayout
)

class MillingApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Розрахунок режимів фрезерування")
        self.resize(600, 600)

        main_layout = QVBoxLayout()

        parameters_group = QGroupBox("Параметри фрезерування")
        parameters_layout = QFormLayout()

        self.processing_type_combo = QComboBox()
        self.processing_type_combo.addItems(["Чорнова", "Чистова"])
        parameters_layout.addRow(QLabel("Тип обробки:"), self.processing_type_combo)

        self.material_combo = QComboBox()
        self.material_combo.addItems(["Сталь конструкційна Т5К12В", "Сталь конструкційна Т5К10", "Сталь конструкційна P18",
                                      "Сталь конструкційна Т15К6", "Сталь конструкційна Р6М5", "Сталь конструкційна Т30К4",
                                      "Сталь конструкційна ВК8", "Сталь загартована Т15К6 HRC 35-50", "Сталь загартована Т30К4 HRC 35-50",
                                      "Сталь загартована ВК6 HRC 35-50", "Сталь загартована ВК8 HRC 35-50",
                                      "Сталь загартована ВК4 HRC 51-62", "Сталь загартована ВК6 HRC 51-62", "Сталь загартована ВК8 HRC 51-62",
                                      "Чавун ВК8 HRC 35-50", "Чавун ВК6 HRC 35-50", "Чавун ВК4 HRC 35-50",
                                      "Чавун ВК3 HRC 35-50", "Чавун Р18 HRC 51-62", "Чавун Р6М3 HRC 51-62",
                                      "Мідь або алюніній Р6М5 HRC 35-50", "Мідь або алюніній ВК4 HRC 35-50",
                                      "Мідь або алюніній ВК6 HRC 35-50", "Мідь або алюніній 9ХС HRC 35-50",
                                      "Мідь або алюніній ХВГ HRC 51-62", "Мідь або алюніній У12А HRC 51-62",])
        parameters_layout.addRow(QLabel("Матеріал заготовки:"), self.material_combo)

        self.tool_type_combo = QComboBox()
        self.tool_type_combo.addItems(["Торцева", "Циліндрична", "Дискова", "Кінцева"])
        parameters_layout.addRow(QLabel("Тип фрези:"), self.tool_type_combo)

        self.tool_subtype_1_label = QLabel("Вид фрези:")
        self.tool_subtype_1_combo = QComboBox()
        self.tool_subtype_1_combo.addItems(["Зі вставними ножами", "Цілісна"])
        parameters_layout.addRow(self.tool_subtype_1_label, self.tool_subtype_1_combo)

        self.tool_subtype_2_label = QLabel("Вид фрези:")
        self.tool_subtype_2_combo = QComboBox()
        self.tool_subtype_2_combo.addItems(["З коронками", "З напаяними пластинами", "Цілісна"])
        parameters_layout.addRow(self.tool_subtype_2_label, self.tool_subtype_2_combo)

        self.tool_subtype_1_label.setVisible(False)
        self.tool_subtype_1_combo.setVisible(False)
        self.tool_subtype_2_label.setVisible(False)
        self.tool_subtype_2_combo.setVisible(False)
        self.tool_type_combo.currentTextChanged.connect(self.update_visibility)




        self.tool_material_label = QLabel("Матеріал фрези:")
        self.tool_material_combo = QComboBox()
        self.tool_material_combo.addItems(["Твердий сплав", "Швидкорізальна сталь"])
        parameters_layout.addRow(self.tool_material_label, self.tool_material_combo)

        self.tool_material_combo.setVisible(True)
        self.tool_material_label.setVisible(True)
        self.tool_type_combo.currentTextChanged.connect(self.update_visibility)
        self.tool_material_combo.currentTextChanged.connect(self.update_visibility)

        self.tooth_size_label = QLabel("Розмір зуба фрези:")
        self.tooth_size_large = QRadioButton("Великий")
        self.tooth_size_small = QRadioButton("Дрібний")
        self.tooth_size_group = QButtonGroup()
        self.tooth_size_group.addButton(self.tooth_size_large)
        self.tooth_size_group.addButton(self.tooth_size_small)
        tooth_size_layout = QHBoxLayout()
        tooth_size_layout.addWidget(self.tooth_size_large)
        tooth_size_layout.addWidget(self.tooth_size_small)
        parameters_layout.addRow(self.tooth_size_label, tooth_size_layout)

        self.tooth_size_label.setVisible(False)
        self.tooth_size_large.setVisible(False)
        self.tooth_size_small.setVisible(False)
        self.processing_type_combo.currentTextChanged.connect(self.update_visibility)
        self.tool_type_combo.currentTextChanged.connect(self.update_visibility)

        self.processing_type_combo.currentTextChanged.connect(self.update_visibility)
        self.tool_type_combo.currentTextChanged.connect(self.update_visibility)
        self.tool_material_combo.currentTextChanged.connect(self.update_visibility)


        self.tool_diameter_input = QLineEdit()
        parameters_layout.addRow(QLabel("Діаметр фрези, мм:"), self.tool_diameter_input)

        self.teeth_number_input = QLineEdit()
        parameters_layout.addRow(QLabel("Кількість зубів фрези:"), self.teeth_number_input)

        self.milling_width_input = QLineEdit()
        parameters_layout.addRow(QLabel("Ширина фрезерування, мм:"), self.milling_width_input)

        self.milling_depth_input = QLineEdit()
        parameters_layout.addRow(QLabel("Припуск на обробку, мм:"), self.milling_depth_input)

        self.surface_state_combo = QComboBox()
        self.surface_state_combo.addItems(["Без кірки", "Прокат з кіркою", "Поковка з кіркою", "Мідні та алюмінієві сплави з кіркою",
                                           "Сталеві та чавунні відливання з нормальною кіркою", "Сталеві та чавунні відливання з забрудненою кіркою"])
        parameters_layout.addRow(QLabel("Стан поверхні заготовки:"), self.surface_state_combo)

        self.material_strength_label = QLabel("Межа міцності / твердість (МПа):")
        self.material_strength_input = QLineEdit()
        parameters_layout.addRow(self.material_strength_label, self.material_strength_input)
        self.material_strength_label.setVisible(True)
        self.material_strength_input.setVisible(True)
        self.material_combo.currentTextChanged.connect(self.update_visibility)

        self.workbench_power_label = QLabel("Потужність верстата (кВт):")
        self.workbench_power_less = QRadioButton("<5 кВт")
        self.workbench_power_mid = QRadioButton("5-10 кВт")
        self.workbench_power_more = QRadioButton(">10 кВт")
        self.workbench_power_group = QButtonGroup()
        self.workbench_power_group.addButton(self.workbench_power_less)
        self.workbench_power_group.addButton(self.workbench_power_mid)
        self.workbench_power_group.addButton(self.workbench_power_more)
        workbench_power_layout = QHBoxLayout()
        workbench_power_layout.addWidget(self.workbench_power_less)
        workbench_power_layout.addWidget(self.workbench_power_mid)
        workbench_power_layout.addWidget(self.workbench_power_more)
        parameters_layout.addRow(self.workbench_power_label, workbench_power_layout)

        self.workbench_power_label.setVisible(True)
        self.workbench_power_less.setVisible(True)
        self.workbench_power_mid.setVisible(True)
        self.workbench_power_more.setVisible(True)
        self.processing_type_combo.currentTextChanged.connect(self.update_visibility)
        self.tool_type_combo.currentTextChanged.connect(self.update_visibility)

        parameters_group.setLayout(parameters_layout)
        """
        size_group = QGroupBox("Розміри заготовки (мм)")
        size_layout = QFormLayout()

        self.length_input = QLineEdit()
        size_layout.addRow(QLabel("Довжина:"), self.length_input)

        self.width_input = QLineEdit()
        size_layout.addRow(QLabel("Ширина:"), self.width_input)

        self.height_input = QLineEdit()
        size_layout.addRow(QLabel("Висота:"), self.height_input)

        size_group.setLayout(size_layout)"""

        calculate_button = QPushButton("Розрахувати")

        results_group = QGroupBox("Результати розрахунку")
        results_layout = QFormLayout()

        self.result_depth = QLabel("-")
        results_layout.addRow(QLabel("Глибина, мм:"), self.result_depth)

        self.result_feed_rate = QLabel("-")
        self.feed_rate_label = QLabel("Подача на зуб, мм/зуб:")
        self.processing_type_combo.currentTextChanged.connect(self.update_text)
        results_layout.addRow(self.feed_rate_label, self.result_feed_rate)

        self.result_cutting_speed = QLabel("-")
        results_layout.addRow(QLabel("Швидкість різання, м/хв:"), self.result_cutting_speed)

        self.result_spindle_speed = QLabel("-")
        results_layout.addRow(QLabel("Частота обертання, об/хв:"), self.result_spindle_speed)

        results_group.setLayout(results_layout)

        main_layout.addWidget(parameters_group)
        """main_layout.addWidget(size_group)"""
        main_layout.addWidget(calculate_button)
        main_layout.addWidget(results_group)

        self.setLayout(main_layout)

        self.calculate_button = calculate_button

        self.material_category_map = {
            "Сталь конструкційна Т5К12В": "Сталь та чавун",
            "Сталь конструкційна Т5К10": "Сталь та чавун",
            "Сталь конструкційна P18": "Сталь та чавун",
            "Сталь конструкційна Т15К6": "Сталь та чавун",
            "Сталь конструкційна Р6М5": "Сталь та чавун",
            "Сталь конструкційна Т30К4": "Сталь та чавун",
            "Сталь конструкційна ВК8": "Сталь та чавун",
            "Сталь загартована Т15К6 HRC 35-50": "Сталь та чавун",
            "Сталь загартована Т30К4 HRC 35-50": "Сталь та чавун",
            "Сталь загартована ВК6 HRC 35-50": "Сталь та чавун",
            "Сталь загартована ВК8 HRC 35-50": "Сталь та чавун",
            "Сталь загартована ВК4 HRC 51-62": "Сталь та чавун",
            "Сталь загартована ВК6 HRC 51-62": "Сталь та чавун",
            "Сталь загартована ВК8 HRC 51-62": "Сталь та чавун",

            "Чавун ВК8 HRC 35-50": "Сталь та чавун",
            "Чавун ВК6 HRC 35-50": "Сталь та чавун",
            "Чавун ВК4 HRC 35-50": "Сталь та чавун",
            "Чавун ВК3 HRC 35-50": "Сталь та чавун",
            "Чавун Р18 HRC 51-62": "Сталь та чавун",
            "Чавун Р6М3 HRC 51-62": "Сталь та чавун",

            "Мідь або алюніній Р6М5 HRC 35-50": "Мідь та алюміній",
            "Мідь або алюніній ВК4 HRC 35-50": "Мідь та алюміній",
            "Мідь або алюніній ВК6 HRC 35-50": "Мідь та алюміній",
            "Мідь або алюніній 9ХС HRC 35-50": "Мідь та алюміній",
            "Мідь або алюніній ХВГ HRC 51-62": "Мідь та алюміній",
            "Мідь або алюніній У12А HRC 51-62": "Мідь та алюміній",
        }
    def update_text(self):

        is_roughing = self.processing_type_combo.currentText() == "Чорнова"
        if (is_roughing):
            self.feed_rate_label.setText("Подача на зуб, мм/зуб:")
        else:
            self.feed_rate_label.setText("Подача на оберт, мм/об:")

    def update_visibility(self):
        is_roughing = self.processing_type_combo.currentText() == "Чорнова"

        is_end_mill_2 = self.tool_type_combo.currentText() in ["Торцева", "Циліндрична", "Дискова"]
        self.tool_material_combo.setVisible(is_end_mill_2)
        self.tool_material_label.setVisible(is_end_mill_2)

        is_tool_material = self.tool_material_combo.currentText() == "Швидкорізальна сталь"
        tooth_size_visible = is_roughing and is_tool_material and is_end_mill_2
        self.tooth_size_label.setVisible(tooth_size_visible)
        self.tooth_size_large.setVisible(tooth_size_visible)
        self.tooth_size_small.setVisible(tooth_size_visible)

        is_workbench_power = is_roughing and is_end_mill_2
        self.workbench_power_label.setVisible(is_workbench_power)
        self.workbench_power_less.setVisible(is_workbench_power)
        self.workbench_power_mid.setVisible(is_workbench_power)
        self.workbench_power_more.setVisible(is_workbench_power)

        material = self.material_category_map[self.material_combo.currentText()]
        if (material == "Мідь та алюміній"):
            self.material_strength_label.setVisible(False)
            self.material_strength_input.setVisible(False)
        else:
            self.material_strength_label.setVisible(True)
            self.material_strength_input.setVisible(True)

        if (self.tool_type_combo.currentText() == "Дискова"):
            self.tool_subtype_1_label.setVisible(True)
            self.tool_subtype_1_combo.setVisible(True)
            self.tool_subtype_2_label.setVisible(False)
            self.tool_subtype_2_combo.setVisible(False)

        elif (self.tool_type_combo.currentText() == "Кінцева"):
            self.tool_subtype_1_label.setVisible(False)
            self.tool_subtype_1_combo.setVisible(False)
            self.tool_subtype_2_label.setVisible(True)
            self.tool_subtype_2_combo.setVisible(True)
        else:
            self.tool_subtype_1_label.setVisible(False)
            self.tool_subtype_1_combo.setVisible(False)
            self.tool_subtype_2_label.setVisible(False)
            self.tool_subtype_2_combo.setVisible(False)
