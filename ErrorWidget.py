from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PySide6.QtCore import Signal

class ErrorWidget(QWidget):
    close_Signal = Signal()

    def __init__(self, msg: str):
        super().__init__()

        with open('log.txt', 'a') as f:
            f.write(f'main: {msg} \n')

        self.msg = msg
        
        self.mainLayout = QVBoxLayout()

        self.msg_label = QLabel(self.msg)

        self.button = QPushButton('ok', self)
        self.button.clicked.connect(lambda: self.close_Signal.emit())

        self.mainLayout.addWidget(self.msg_label)
        self.mainLayout.addWidget(self.button)

        self.setLayout(self.mainLayout)