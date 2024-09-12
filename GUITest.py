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
        self.unit_stats = QLabel("Placeholder", self)
        self.button = QPushButton("Create Random Character", self)
        self.exit = QPushButton("Exit", self)

        self.initUI()
        


    def initUI(self):

        self.setWindowTitle("Hayden Tactics")

        self.is_running = True

        grid = QGridLayout()
        grid.addWidget(self.list1)
        grid.addWidget(self.button)
        grid.addWidget(self.unit_stats)
        grid.addWidget(self.exit)

        self.list1.setGeometry(0, 0, 200, 200)
        self.unit_stats.setGeometry(0, 0, 500, 500)
        #self.button.setGeometry(0, 200, 100, 100)
        #self.button.setStyleSheet("font-size: 25px;"
        #                          "font-family: Arial")


        self.setLayout(grid)

        self.button.clicked.connect(self.display_random_unit)

        #self.list1.itemSelectionChanged.connect(self.selection_changed)
        self.list1.itemClicked.connect(self.selection_changed)



    def selection_changed(self):

        unit = self.get_selected_unit()

        unit_stats = Unit.display_unit(unit)

        self.unit_stats.setText(unit_stats)


    def get_selected_unit(self):

        item = self.list1.currentItem()

        unit_id = int(item.text().split(' ')[0])
        unit = Unit.get_unit_by_id(unit_id)

        return unit
        



    def display_random_unit(self):
        unit = Unit.generate_random_unit()
        #print(f"created {unit.name}")

        self.list1.clear()

        for unit in Unit.unitlist:
            #item = QListWidgetItem(unit.id, unit.name)
            #self.list1.addItem(item)
            self.list1.addItem(f"{unit.id} {unit.name}")

            

        #self.unit_stats.text("Blah")

        

    #def display_unit_stats(self):


if __name__ == '__main__':
    app = QApplication(sys.argv)
    unit_gui = UnitGUI()
    unit_gui.show()
    sys.exit(app.exec_())