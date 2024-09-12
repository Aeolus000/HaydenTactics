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
        self.unit_stats = QLabel(self)
        self.button = QPushButton("Create Random Character", self)
        self.level_up_button = QPushButton("Level Up", self)
        self.dismiss_unit_button = QPushButton("Dismiss Unit", self)
        #self.confirm_dismiss_button = QDialogButtonBox(self)
        #self.exit = QPushButton("Exit", self)

        self.initUI()
        


    def initUI(self):

        self.setWindowTitle("Hayden Tactics")

        grid = QGridLayout()
        grid.addWidget(self.list1, 0, 0)
        grid.addWidget(self.button)
        grid.addWidget(self.unit_stats, 0, 1)
        #grid.addWidget(self.exit)
        grid.addWidget(self.level_up_button, 1, 1)
        grid.addWidget(self.dismiss_unit_button, 2, 1)

        self.list1.setGeometry(0, 0, 200, 200)
        self.unit_stats.setGeometry(100, 100, 400, 600)

        self.setLayout(grid)

        self.button.clicked.connect(self.display_random_unit)

        self.level_up_button.clicked.connect(self.display_level_up)

        self.list1.itemClicked.connect(self.selection_changed)

        self.dismiss_unit_button.setDisabled(True)
        self.level_up_button.setDisabled(True)
        self.dismiss_unit_button.clicked.connect(self.dismiss_unit)

    def selection_changed(self):

        unit = self.get_selected_unit()

        unit_stats = Unit.display_unit(unit, 2)

        self.unit_stats.setText(unit_stats)


        if self.list1.currentItem() == None:
            self.dismiss_unit_button.setDisabled(True)
            self.level_up_button.setDisabled(True)
        else:
            self.dismiss_unit_button.setDisabled(False)
            self.level_up_button.setDisabled(False)

        if unit.level >= 30:
            self.level_up_button.setDisabled(True)
        else:
            self.level_up_button.setDisabled(False)

        
    def refresh_unit_list(self):
        self.list1.clear()
        for unit in Unit.unitlist:
            self.list1.addItem(f"{unit.id} {unit.name}")

    def get_selected_unit(self):

        item = self.list1.currentItem()

        unit_id = int(item.text().split(' ')[0])
        unit = Unit.get_unit_by_id(unit_id)

        return unit
        

    def display_random_unit(self):
        unit = Unit.generate_random_unit()
        #print(f"created {unit.name}")

        self.refresh_unit_list()

    def display_level_up(self):
        unit = self.get_selected_unit()

        Unit.level_up(unit)

        self.selection_changed()

    def dismiss_unit(self):
        unit = self.get_selected_unit()
        Unit.unitlist.remove(unit)

        self.refresh_unit_list()

        self.list1.setCurrentItem(None)
        self.dismiss_unit_button.setDisabled(True)
        self.level_up_button.setDisabled(True)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    unit_gui = UnitGUI()
    unit_gui.show()
    sys.exit(app.exec_())