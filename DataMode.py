import json

class DataMode():
    def __init__(self):
        self.loadData()

    def loadData(self) -> dict:
        with open('./data.json', 'r') as f:
            self.data = json.loads(f.read())
        return self.data

    def updateData(self):
        with open('./data.json', 'w') as f:
            json.dump(self.data, f)

if __name__ == '__main__':
    dm = DataMode()
    dm.loadData()