# gui/main_window.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QLineEdit,
    QFormLayout, QGroupBox
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
        self.processing_type_combo.addItems(["Чорнова", "Напівчистова", "Чистова"])
        parameters_layout.addRow(QLabel("Тип обробки:"), self.processing_type_combo)

        self.processing_type_combo = QComboBox()
        self.processing_type_combo.addItems(["Фрезерування площин", "Фрезерування пазів", "Чистова"])
        parameters_layout.addRow(QLabel("Тип операції:"), self.processing_type_combo)

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

        self.tool_material_combo = QComboBox()
        self.tool_material_combo.addItems(["Твердий сплав", "Швидкорізальна сталь"])
        parameters_layout.addRow(QLabel("Матеріал фрези:"), self.tool_material_combo)

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

        self.material_strength_input = QLineEdit()
        parameters_layout.addRow(QLabel("Межа міцності / твердість (МПа):"), self.material_strength_input)

        self.surface_state_combo = QComboBox()
        self.surface_state_combo.addItems(
            ["< 10 кВт", "> 10 кВт"])
        parameters_layout.addRow(QLabel("Потужність верстата (кВт):"), self.surface_state_combo)

        parameters_group.setLayout(parameters_layout)

        size_group = QGroupBox("Розміри заготовки (мм)")
        size_layout = QFormLayout()

        self.length_input = QLineEdit()
        size_layout.addRow(QLabel("Довжина:"), self.length_input)

        self.width_input = QLineEdit()
        size_layout.addRow(QLabel("Ширина:"), self.width_input)

        self.height_input = QLineEdit()
        size_layout.addRow(QLabel("Висота:"), self.height_input)

        size_group.setLayout(size_layout)

        calculate_button = QPushButton("Розрахувати")

        results_group = QGroupBox("Результати розрахунку")
        results_layout = QFormLayout()

        self.result_feed_rate = QLabel("-")
        results_layout.addRow(QLabel("Глибина, мм:"), self.result_feed_rate)

        self.result_feed_rate = QLabel("-")
        results_layout.addRow(QLabel("Подача, мм/хв:"), self.result_feed_rate)

        self.result_cutting_speed = QLabel("-")
        results_layout.addRow(QLabel("Швидкість різання, м/хв:"), self.result_cutting_speed)

        self.result_spindle_speed = QLabel("-")
        results_layout.addRow(QLabel("Частота обертання, об/хв:"), self.result_spindle_speed)

        results_group.setLayout(results_layout)

        main_layout.addWidget(parameters_group)
        main_layout.addWidget(size_group)
        main_layout.addWidget(calculate_button)
        main_layout.addWidget(results_group)

        self.setLayout(main_layout)

        self.calculate_button = calculate_button