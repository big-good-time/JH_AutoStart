from MainWindow import MainWindow
from PySide6.QtWidgets import QApplication
from DataMode import DataMode
import sys

if __name__ == '__main__':
    dataMode = DataMode()

    app = QApplication(sys.argv)
    window = MainWindow(dataMode)
    window.show()
    sys.exit(app.exec())