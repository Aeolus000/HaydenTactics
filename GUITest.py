import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import Unit
import Stats
import Items



class UnitGUI(QWidget):
    def __init__(self):
        super().__init__()
        #self.setGeometry(700, 300, 500, 500)
        self.list1 = QListWidget(self)
        self.unit_stats = QLabel(self)
        self.button = QPushButton("Create Random Character", self)
        self.level_up_button = QPushButton("Level Up", self)
        self.dismiss_unit_button = QPushButton("Dismiss Unit", self)
        self.message = QLabel(self)
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
        grid.addWidget(self.message, 0, 2)

        self.list1.setGeometry(0, 0, 200, 200)
        self.unit_stats.setGeometry(100, 100, 400, 600)

        self.message.setStyleSheet("font-family: calibri; font-size: 20px")

        self.setLayout(grid)

        self.button.clicked.connect(self.display_random_unit)

        self.level_up_button.setDisabled(True)
        self.level_up_button.clicked.connect(self.display_level_up)

        self.list1.itemClicked.connect(self.selection_changed)

        self.dismiss_unit_button.setDisabled(True)
        self.dismiss_unit_button.clicked.connect(self.dismiss_unit)

        self.refresh_unit_list()




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
        inventory_gui.refresh_unit_list()

        self.dismiss_unit_button.setDisabled(True)
        self.level_up_button.setDisabled(True)

    def display_level_up(self):
        unit = self.get_selected_unit()

        Unit.level_up(unit)
        self.message.setText(f"{unit.name} has leveled up to Level {unit.level}!")

        self.selection_changed()

    def dismiss_unit(self):
        unit = self.get_selected_unit()
        Unit.unitlist.remove(unit)

        self.refresh_unit_list()
        inventory_gui.refresh_unit_list()

        self.list1.setCurrentItem(None)
        self.unit_stats.clear()
        self.dismiss_unit_button.setDisabled(True)
        self.level_up_button.setDisabled(True)


class InventoryGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Inventory Management")


        self.unit_list = QListWidget(self)
        self.inventory_list = QListWidget(self)
        self.unit_equip_list = QListWidget(self)
        self.item_stats_label = QLabel("Item Stats", self)
        self.equip_button = QPushButton("Equip Item", self)
        self.unequip_button = QPushButton("Unequip Item", self)

        self.weapon_slots_label = QLabel("Weapon Slot 1: ", self)

        self.inventory_label = QLabel("Inventory", self)
        self.unit_list_label = QLabel("Unit List", self)
        self.unit_equip_label = QLabel("Unit Equipment", self)

        self.initUI()

    def initUI(self):

        grid = QGridLayout()

        grid.addWidget(self.unit_list, 1, 0)
        grid.addWidget(self.unit_equip_list, 1, 1)
        grid.addWidget(self.inventory_list, 1, 2)
        grid.addWidget(self.item_stats_label, 1, 3)
        grid.addWidget(self.equip_button, 2, 2)
        grid.addWidget(self.unequip_button, 2, 1)

        grid.addWidget(self.unit_list_label, 0, 0)
        grid.addWidget(self.unit_equip_label, 0, 1)
        grid.addWidget(self.inventory_label, 0, 2)

        self.unit_list_label.setAlignment(Qt.AlignCenter)
        self.inventory_label.setAlignment(Qt.AlignCenter)
        self.unit_equip_label.setAlignment(Qt.AlignCenter)

        self.setLayout(grid)

        self.unit_list.itemClicked.connect(self.selection_changed_unit_list)
        self.unit_equip_list.itemClicked.connect(self.selection_changed_equipment_list)
        self.inventory_list.itemClicked.connect(self.selection_changed_inventory_list)


        self.unequip_button.setDisabled(True)
        self.unequip_button.clicked.connect(self.unequip_equipment)


        self.refresh_equipment_list()
        self.refresh_inventory_list()
        self.refresh_unit_list()




    def refresh_unit_list(self):
        self.unit_list.clear()
        for unit in Unit.unitlist:
            self.unit_list.addItem(f"{unit.id} {unit.name}")

    def refresh_equipment_list(self):
        self.unit_equip_list.clear()
        if self.unit_list.currentItem():
            unit = self.get_selected_unit()
        

            unit_equipment = unit.get_equipment_as_dict()

            for item in unit_equipment.values():
                if item:
                    self.unit_equip_list.addItem(f"{item.name}")


    def refresh_inventory_list(self):
        self.inventory_list.clear()
        #inventory = items_inventory
        for item in items_inventory.items:
            self.inventory_list.addItem(f"{item.name}")

    def get_selected_unit(self):

        item = self.unit_list.currentItem()

        unit_id = int(item.text().split(' ')[0])
        unit = Unit.get_unit_by_id(unit_id)

        return unit
    
    def get_selected_equipment(self):

        unit = self.get_selected_unit()
        #print(unit)

        selected_equipment = self.unit_equip_list.currentItem()

        selected_equipment = selected_equipment.data(2)
        #print(selected_equipment)                                        # selected_equipment is "Iron Short Sword" as a string

        unit_equipment = unit.get_equipment_as_dict()

        for item in unit_equipment.values():
            if item:
                if item.name == selected_equipment:
                    selected_equipment = item      
                    #print(selected_equipment)                            # selected_equipment is becoming the Weapon object, because it's Weapon.name is matching the string from the ListItem Object


        return selected_equipment
    
    def get_selected_inventory_item(self):
        
        inv_item = self.inventory_list.currentItem()
        inv_item = inv_item.data(2)

        for item in items_inventory.items:
            if inv_item == item.name:
                inv_item = item



        return inv_item
    
    def selection_changed_unit_list(self):

        unit = self.get_selected_unit()
        self.item_stats_label.setText(Unit.display_unit(unit, 3))
        self.refresh_equipment_list()
        self.refresh_inventory_list()


    def selection_changed_equipment_list(self):

        if self.unit_equip_list.currentItem() == None:
            self.unequip_button.setDisabled(True)

        else:
            self.unequip_button.setDisabled(False)
            equipment = self.get_selected_equipment()
            self.item_stats_label.setText(equipment.display_stats(equipment))
            self.refresh_inventory_list()

    def selection_changed_inventory_list(self):

        if self.inventory_list.currentItem() == None:
            self.equip_button.setDisabled(True)

        else:
            self.equip_button.setDisabled(False)
            inv_item = self.get_selected_inventory_item()
            self.item_stats_label.setText(inv_item.display_stats(inv_item))
        


        
        
    def equip_equipment(self):
        pass

    def unequip_equipment(self):

        unit = self.get_selected_unit()
        item = self.get_selected_equipment()

        #print(item.slot_type)

        item.unequip(unit, item.slot_type, items_inventory)

        #print(item.slot_type)

        self.selection_changed_unit_list()
        self.unequip_button.setDisabled(True)

        self.refresh_inventory_list()
        self.refresh_equipment_list()









if __name__ == '__main__':

    #unit_gui.show()

        ## testing by creating a bunch of stuff
    Unit.generate_random_unit()
    Unit.generate_random_unit()
    unittest = Unit.generate_random_unit()
    items_inventory = Items.Inventory(50)
    weapon = Items.Weapon("Iron Short Sword", 4, 50, "one-handed", "Slashing", 6)
    weapon2 = Items.Weapon("Iron Short Sword", 4, 50, "one-handed", "Slashing", 6)
    items_inventory.items.append(weapon)
    items_inventory.items.append(weapon2)
    weapon.equip(unittest, "weaponslot3", items_inventory)

    armor = Items.Armor("Armor lol", 1, 1, "Blah")
    items_inventory.items.append(armor)
    armor.equip(unittest, "armorslot", items_inventory)



    app = QApplication(sys.argv)
    unit_gui = UnitGUI()
    unit_gui.show()
    inventory_gui = InventoryGUI()
    inventory_gui.show()
    sys.exit(app.exec_())