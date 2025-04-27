# main.py
import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MillingApp

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MillingApp()
    window.show()

    sys.exit(app.exec())
