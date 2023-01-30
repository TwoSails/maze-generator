from mazeGenerator import App


class Controller:
    def __init__(self):
        self.app = App()
        self.inputData = {}
        self.fetch = {"RuntimeBool": False,
                      "SeedBool": False,
                      "LogBool": False,
                      "SeedStr": "",
                      "WidthInt": 0,
                      "HeightInt": 0,
                      "GenerationsInt": 0}
        self.components = {}

    def addComponent(self, tag, component):
        self.components[tag] = component
        if tag in self.fetch.keys():
            self.inputData[tag] = component.fetchData

    def convertBoardToCanvas(self):
        pass

    def assign_fetch(self):
        pass

    def gather_data(self):
        for tag in self.inputData.keys():
            if tag in self.fetch.keys():
                self.fetch[tag] = self.inputData[tag]()

        print(self.fetch)

    def button_run(self):
        self.gather_data()

    def button_downloadPDF(self):
        pass

    def button_downloadPNG(self):
        pass

    def button_pausePlay(self):
        pass
