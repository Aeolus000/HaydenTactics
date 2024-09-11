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
        self.list1 = QListWidget(self)
        self.button = QPushButton("Create", self)
        self.setWindowTitle("Hayden Tactics")
        self.initUI()

    def initUI(self):

        #selected_unit = self.list1.clicked(self.selected_item)
        self.list1.setGeometry(0, 0, 200, 200)
        self.button.setGeometry(0, 200, 100, 100)
        self.button.setStyleSheet("font-size: 25px;"
                                  "font-family: Arial")



        label1 = QLabel("Unit")


        #grid = QGridLayout()
        #grid.addWidget(label1, 0, 1)
        #grid.addWidget(self.list1, 0, 0)

        self.button.clicked.connect(self.selected_item)

    def selected_item(self):
        unit = Unit.generate_random_unit()
        print(f"created {unit.name}")

        self.list1.clear()

        for unit in Unit.unitlist:
            self.list1.addItem(f"{unit.id} {unit.name}")


def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()