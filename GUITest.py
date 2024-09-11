import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import Unit
import Stats



class UnitGUI(QWidget):
    def __init__(self):
        super().__init__()
        #self.setGeometry(700, 300, 500, 500)
        self.list1 = QListWidget(self)
        self.button = QPushButton("Create Random Character", self)

        self.initUI()

    def initUI(self):

        self.setWindowTitle("Hayden Tactics")

        grid = QGridLayout()
        grid.addWidget(self.list1)
        grid.addWidget(self.button)

        self.list1.setGeometry(0, 0, 200, 200)
        #self.button.setGeometry(0, 200, 100, 100)
        #self.button.setStyleSheet("font-size: 25px;"
        #                          "font-family: Arial")


        self.setLayout(grid)

        self.button.clicked.connect(self.selected_item)

    def selected_item(self):
        unit = Unit.generate_random_unit()
        print(f"created {unit.name}")

        self.list1.clear()

        for unit in Unit.unitlist:
            self.list1.addItem(f"{unit.id} {unit.name}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    unit_gui = UnitGUI()
    unit_gui.show()
    sys.exit(app.exec_())