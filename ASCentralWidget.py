from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtGui import QIntValidator
from PySide6.QtCore import Qt, Signal
from functools import partial
from DataMode import DataMode
from PathLine import PathLine

class ASCentralWidget(QWidget):
    sig_handStart = Signal()
    sig_quitAuto = Signal()
    sig_breakWait = Signal()
    sig_pathEdit = Signal()

    def __init__(self, dataMode: DataMode):
        super().__init__()

        self.index = 0
        self.dataMode = dataMode

        self.pathLineList = []

        self.setupUi()

    def setupUi(self):
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.mainLayout)
        self.setTopLayout()
        self.setContentLayout()

    def setTopLayout(self):
        """
        设置第一排的配置信息和启动按钮
        """
        
        self.waitTimeLabel = QLabel('前置时间', self)
        self.waitTimeEdit = QLineEdit(str(self.dataMode.data['waitTime']), self)
        self.waitTimeEdit.setValidator(QIntValidator(0, 1000)) # 限制输入数字为 0-1000
        self.waitTimeEdit.textEdited.connect(self.timeEdit)

        self.spaceTimeLabel = QLabel('启动间隔', self)
        self.spaceTimeEdit = QLineEdit(str(self.dataMode.data['spaceTime']), self)
        self.spaceTimeEdit.setValidator(QIntValidator(0, 1000)) # 限制输入数字为 0-1000
        self.spaceTimeEdit.textEdited.connect(self.timeEdit)

        self.handStartButton = QPushButton('手动开始', self)
        self.handStartButton.clicked.connect(lambda: self.sig_handStart.emit())
        self.handStartButton.setEnabled(False)
        
        self.quitAutoButton = QPushButton('退出自动', self)
        self.quitAutoButton.clicked.connect(lambda: self.sig_quitAuto.emit())

        self.breakWaitButton = QPushButton('跳出等待', self)
        self.breakWaitButton.clicked.connect(lambda: self.sig_breakWait.emit())

        self.topLayout = QHBoxLayout()
        self.topLayout.addWidget(self.waitTimeLabel)
        self.topLayout.addWidget(self.waitTimeEdit)
        self.topLayout.addWidget(self.spaceTimeLabel)
        self.topLayout.addWidget(self.spaceTimeEdit)
        self.topLayout.addWidget(self.handStartButton)
        self.topLayout.addWidget(self.quitAutoButton)
        self.topLayout.addWidget(self.breakWaitButton)
        self.mainLayout.addLayout(self.topLayout)

    def setContentLayout(self):
        """ 设置软件位置列表 """
        self.pathTip = QLabel('位置', self)
        self.pathTip.setFixedSize(self.dataMode.data['pathEditWidth'], 20)
        self.pathTip.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.pathTip.setStyleSheet('background-color: red')

        self.noteTip = QLabel('备注', self)
        self.noteTip.setFixedSize(self.dataMode.data['noteEditWidth'], 20)
        self.noteTip.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.noteTip.setStyleSheet('background-color: red')

        noteLayout = QHBoxLayout()
        noteLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        noteLayout.addWidget(self.pathTip)
        noteLayout.addWidget(self.noteTip)


        self.contentLayout = QVBoxLayout()
        self.contentLayout.addLayout(noteLayout)

        for i in range(len(self.dataMode.data['pathList'])):
            path = self.dataMode.data['pathList'][i][0]
            note = self.dataMode.data['pathList'][i][1]
            self.addPath2List(False, path, note)


        self.mainLayout.addLayout(self.contentLayout)

        self.ADLayout = QHBoxLayout()
        self.addButton = QPushButton('+')
        self.addButton.clicked.connect(partial(self.addPath2List, isNew=True))
        self.delButton = QPushButton('-')
        self.delButton.clicked.connect(self.delPath2List)
        self.ADLayout.addWidget(self.addButton)
        self.ADLayout.addWidget(self.delButton)
        self.mainLayout.addLayout(self.ADLayout)
    
    def addPath2List(self, isNew: bool = False, path: str = '', note: str = ''):
        """添加"""
        print(f'new: {self.index}')
        if isNew:
            self.dataMode.data['pathList'].append([path, note])
            self.dataMode.updateData()
        else:
            self.sig_pathEdit.emit()
        layout = PathLine(self.dataMode, self.index, path, note)
        self.contentLayout.addLayout(layout)
        self.pathLineList.append(layout)
        self.dataMode.updateData()
        self.index += 1

    
    def delPath2List(self):
        """删除"""
        if self.index == 0: return

        del self.dataMode.data['pathList'][-1]
        del self.pathLineList[-1]
        self.dataMode.updateData()
        layout = self.contentLayout.itemAt(self.contentLayout.count() - 1)
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.contentLayout.removeItem(layout)

        self.sig_pathEdit.emit()

        self.index -= 1
    
    def timeEdit(self):
        """等待时间编辑"""
        if not self.waitTimeEdit.text(): self.waitTimeEdit.setText(str(0))

        if not self.spaceTimeEdit.text(): self.spaceTimeEdit.setText(str(0))

        self.dataMode.data['waitTime'] = int(self.waitTimeEdit.text())
        self.dataMode.data['spaceTime'] = int(self.spaceTimeEdit.text())

        self.dataMode.updateData()
            
        

        
        