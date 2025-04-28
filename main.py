# main.py
import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MillingApp
from logic.milling_calculator import MillingCalculator

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MillingApp()
    calculator = MillingCalculator(window)
    window.show()

    sys.exit(app.exec())
