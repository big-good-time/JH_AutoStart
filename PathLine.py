from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton
from DataMode import DataMode
import os

class PathLine(QHBoxLayout):
    def __init__(self, dataMode: DataMode, index: int, path: str = '', note: str = ''):
        super().__init__()

        self.dataMode = dataMode

        self.index = index

        self.pathEdit = QLineEdit(path)
        self.pathEdit.setFixedWidth(self.dataMode.data['pathEditWidth'])
        self.pathEdit.textChanged.connect(self.textChange)
        self.noteEdit = QLineEdit(note)
        self.noteEdit.setFixedWidth(self.dataMode.data['noteEditWidth'])
        self.noteEdit.textChanged.connect(self.textChange)

        self.startButton = QPushButton('启动')
        self.startButton.clicked.connect(self.start)

        self.addWidget(self.pathEdit)
        self.addWidget(self.noteEdit)
        self.addWidget(self.startButton)
    
    def textChange(self):
        self.dataMode.data['pathList'][self.index][0] = self.pathEdit.text()
        self.dataMode.data['pathList'][self.index][1] = self.noteEdit.text()
        self.dataMode.updateData()
    
    def start(self) -> int:
        try:
            exit_code = os.system(self.pathEdit.text())
            if exit_code == 0:
                self.pathEdit.setStyleSheet('background-color: #77E4C8')
            else:
                self.pathEdit.setStyleSheet('background-color: #FFAAAA')
        except:
            self.pathEdit.setStyleSheet('background-color: #FFAAAA')
        
        return exit_code
        