import json

class DataMode():
    def __init__(self):
        self.loadData()

    def loadData(self) -> dict:
        try:
            with open('./data.json', 'r') as f:
                self.data = json.loads(f.read())
            return self.data
        except:
            self.initData()

    def updateData(self):
        with open('./data.json', 'w') as f:
            json.dump(self.data, f)
    
    def initData(self):
        """重置配置文件"""
        self.data = {"waitTime": 120, "spaceTime": 5, "pathList": [], "pathEditWidth": 400, "noteEditWidth": 100, "windowWidth": 800, "windowHeight": 400}
        self.updateData()


if __name__ == '__main__':
    dm = DataMode()
    dm.loadData()