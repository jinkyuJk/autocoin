import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
###########example 1##########
# print(sys.argv)
# app = QApplication(sys.argv)
# label = QLabel("Hello")
# label.show()
# app.exec_()


####################example2#############
# app = QApplication(sys.argv)
# btn = QPushButton("Hello")
# btn.show()
# app.exec()


###example3###

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(500,500,300,400) #x축,y축, 가로,세로
        self.setWindowTitle("Bitcoin")
        self.setWindowIcon(QIcon("./images/bitcoin.png"))

        btn1 = QPushButton("버튼1",self)
        btn1.move(10,10) # 버튼위치 설정
        btn1.clicked.connect(self.btn_clicked)

        btn2 = QPushButton("버튼2",self)
        btn2.move(10,40)

    def btn_clicked(self):
        print("버튼 클릭")

app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()