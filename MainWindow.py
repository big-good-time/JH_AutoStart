from PySide6.QtWidgets import QMainWindow, QStatusBar, QLabel, QScrollArea
from PySide6.QtCore import QTimer
from collections import deque
from ASCentralWidget import ASCentralWidget
from DataMode import DataMode

class MainWindow(QMainWindow):
    def __init__(self, dataMode: DataMode):
        super().__init__()

        self.dataMode = dataMode
        self.resize(self.dataMode.data['windowWidth'], self.dataMode.data['windowHeight'])
        self.setupUi()
        self.startTimer()
        self.connect()

    def setupUi(self):
        self.contentWidget = ASCentralWidget(self.dataMode)
        self.pathLineQueue = deque(self.contentWidget.pathLineList)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.contentWidget)
        self.setCentralWidget(self.scroll_area)
    
        self.status_bar = QStatusBar() # 状态栏
        self.setStatusBar(self.status_bar)

        self.parmanent_label = QLabel('Ready')
        self.status_bar.addPermanentWidget(self.parmanent_label)

    
    def connect(self):
        self.contentWidget.sig_breakWait.connect(self.breakWait)
        self.contentWidget.sig_handStart.connect(self.handStart)
        self.contentWidget.sig_pathEdit.connect(self.updateQueue)
        self.contentWidget.sig_quitAuto.connect(self.quitAuto)
    
    def updateQueue(self):
        """更新队列"""
        self.pathLineQueue = deque(self.contentWidget.pathLineList)
    
    def breakWait(self):
        """跳出等待"""
        self.quitAuto()
        self.handStart()

    def handStart(self):
        """手动启动"""
        self.contentWidget.handStartButton.setEnabled(False)
        self.contentWidget.quitAutoButton.setEnabled(True)
        self.contentWidget.breakWaitButton.setEnabled(True)
        self.startQueue()
    
    def quitAuto(self):
        """退出自动"""
        self.status_bar.showMessage('结束')
        self.spaceIndex = 0
        self.autoTimer.stop()
        try:
            self.autoTimer.timeout.disconnect()
        except:
            pass
        self.contentWidget.handStartButton.setEnabled(True)
        self.contentWidget.quitAutoButton.setEnabled(False)
        self.contentWidget.breakWaitButton.setEnabled(False)


    def startTimer(self):
        self.index = 1
        self.autoTimer = QTimer()
        self.autoTimer.timeout.connect(self.waitMessage)
        self.autoTimer.start(1100)
    
    def waitMessage(self):
        self.status_bar.showMessage(f'{self.index} / {self.dataMode.data['waitTime']} 秒后启动')
        
        if self.index >= self.dataMode.data['waitTime']:
            self.autoTimer.stop()
            self.autoTimer.timeout.disconnect()
            self.index = 0
            self.startQueue()
        else:
            self.index += 1
    
    def startQueue(self):
        self.spaceIndex = 0

        if len(self.pathLineQueue) == 0:
            self.quitAuto()
            return

        if not self.autoTimer.isActive(): self.pathLineQueue.popleft().start()
        
        self.autoTimer.timeout.connect(self.spaceMessage)
        self.autoTimer.start(1100)
    
    def spaceMessage(self):
        if len(self.pathLineQueue) == 0:
                self.quitAuto()
                return

        self.status_bar.showMessage(f'{self.spaceIndex} / {self.dataMode.data['spaceTime']} 秒后启动下一个')
        if self.spaceIndex >= self.dataMode.data['spaceTime']:
                self.pathLineQueue.popleft().start()
                self.spaceIndex = 0
        else:
            self.spaceIndex += 1



        


        