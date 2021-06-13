from library.data_loader import *


logger.debug("collecter start!")

class Collector:
    print("collector 클래스에 들어왔다")

    def __init__(self):
        print("__Init__함수 ")
        self.collector_api = Coin_data()


    def collecting(self):
        self.collector_api.code_update_check()


if __name__ =='__main__':
    print("__main__에 들어왔습니다")
    c = Collector()
    c.collectiong()