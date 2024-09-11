import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import Unit
import Stats



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(700, 300, 500, 500)
        self.initUI()

    def initUI(self):
        central_widget = QWidget()

        self.setCentralWidget(central_widget)


        list1 = QListWidget()

        Unit.generate_random_unit()
        Unit.generate_random_unit()
        Unit.generate_random_unit()

        for unit in Unit.unitlist:
            list1.addItem(unit.name)
        #list1.addItem("hello")


        label1 = QLabel("Hello")

        label1.setStyleSheet("background-color: red;")

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        grid = QGridLayout()
        
        #vbox.addWidget(label1)
        #vbox.addWidget(list1)
        #hbox.addWidget(label1)

        grid.addWidget(label1, 0, 0)
        grid.addWidget(list1, 0, 1)

        central_widget.setLayout(grid)





def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()