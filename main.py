from MainWindow import MainWindow
from PySide6.QtWidgets import QApplication
from DataMode import DataMode
import sys, ctypes

def run_as_admin():
    try:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if __name__ == '__main__':

    dataMode = DataMode()

    app = QApplication(sys.argv)
    window = MainWindow(dataMode)
    window.show()
    sys.exit(app.exec())