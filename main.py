from MainWindow import MainWindow
from PySide6.QtWidgets import QApplication
from DataMode import DataMode
import sys
from CheckUpdate import CheckUpdate
from ErrorWidget import ErrorWidget

OBJECT_NAME = 'JH_AutoStart' # 项目名称
APP_NAME = 'AutoStart' # 软件名称
VERSION_URL = f'http://127.0.0.1:8000/versions/{OBJECT_NAME}/' # 版本列表
VERSION = '1.0.4' # 当前版本
REQUEST_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
UPDATE_FILE_NAME = 'update.exe'
UPDATE_FILE_URL = f'http://127.0.0.1:8000/update/{UPDATE_FILE_NAME}'


if __name__ == '__main__':

    dataMode = DataMode()
    app = QApplication(sys.argv)

    try:
        is_new_version = CheckUpdate(app,
                                     OBJECT_NAME=OBJECT_NAME,
                                     APP_NAME=APP_NAME,
                                     VERSION_URL=VERSION_URL,
                                     VERSION=VERSION,
                                     REQUEST_USER_AGENT=REQUEST_USER_AGENT,
                                     UPDATE_FILE_NAME=UPDATE_FILE_NAME,
                                     UPDATE_FILE_URL=UPDATE_FILE_URL).check()
        if is_new_version:
            window = MainWindow(dataMode, VERSION)
            window.show()
    except Exception as e:
        window = ErrorWidget(str(e))
        window.close_Signal.connect(lambda: app.exit())
        window.show()
    sys.exit(app.exec())