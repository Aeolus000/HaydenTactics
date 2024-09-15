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

        self.unit_stats.setAlignment(Qt.AlignTop)




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

        self.sync_window_selections()

        
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

        self.list1.setCurrentItem(None)
        self.unit_stats.clear()
        self.dismiss_unit_button.setDisabled(True)
        self.level_up_button.setDisabled(True)

        inventory_gui.equip_button.setDisabled(True)
        inventory_gui.unequip_button.setDisabled(True)

        self.refresh_unit_list()
        inventory_gui.refresh_all()

    def sync_window_selections(self):

        selection = self.list1.currentItem()

        for i in self.list1.findItems("*", Qt.MatchWildcard):                           # i is getting objects
            if i.text() == selection.text():
                select1 = i.text()
                print(select1)


        for i in inventory_gui.unit_list.findItems("*", Qt.MatchWildcard):
            if select1 == i.text():
                inventory_gui.unit_list.setCurrentItem(i)


        # for i in inventory_gui.unit_list.findItems("*", Qt.MatchWildcard):
        #     if i == select1:
        #         select2 = i
        #         print(select2)


        
        # inventory_gui.unit_list.setCurrentItem(select2)



        # unit_list_item = self.list1.selectedItems()

        # print(unit_list_item)

        # unit_text = unit_list_item[0].text()

        # print(unit_list_item[0])

        # inventory_gui.unit_list.setCurrentItem(unit_text)
        



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

        #self.weapon_slots_label = QLabel("Weapon Slot 1: ", self)

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
        self.item_stats_label.setAlignment(Qt.AlignTop)

        self.setLayout(grid)

        self.unit_list.itemClicked.connect(self.selection_changed_unit_list)
        self.unit_equip_list.itemClicked.connect(self.selection_changed_equipment_list)
        self.inventory_list.itemClicked.connect(self.selection_changed_inventory_list)


        self.unequip_button.setDisabled(True)
        self.unequip_button.clicked.connect(self.unequip_equipment)

        self.equip_button.setDisabled(True)
        self.equip_button.clicked.connect(self.equip_equipment)


        self.refresh_all()




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

        for item in items_inventory.items:
            self.inventory_list.addItem(f"{item.name}")



    def refresh_all(self):

        self.refresh_unit_list()
        self.refresh_equipment_list()
        self.refresh_inventory_list()

    def get_selected_unit(self):

        item = self.unit_list.currentItem()

        unit_id = int(item.text().split(' ')[0])
        unit = Unit.get_unit_by_id(unit_id)

        return unit
    
    def get_selected_equipment(self):

        unit = self.get_selected_unit()

        #selected_equipment = self.unit_equip_list.currentItem()

        #selected_equipment = selected_equipment.data(2)

        selected_equipment = self.unit_equip_list.currentRow()
        print(selected_equipment)                                        # selected_equipment is "Iron Short Sword" as a string

        unit_equipment = unit.get_equipment_as_dict()

        unit_equip_indexes = []
        for i in unit_equipment.values():
            if i:
                unit_equip_indexes.append(i.itemid)
                
        print(unit_equip_indexes)

        item_id = unit_equip_indexes[selected_equipment]

        print(item_id)

        selected_equipment = Items.Item.get_item_by_id(item_id, inventory=None, unit=unit)
        
        # for item in unit_equipment.values():
        #     if selected_equipment == unit_equip_indexes[item]:
        #         selected_equipment = item

        # for item in unit_equipment.values():
        #     if item:
        #         if item.name == selected_equipment:
        #             selected_equipment = item      
        #             print(selected_equipment)                            # selected_equipment is becoming the Weapon object, because it's Weapon.name is matching the string from the ListItem Object

        print(selected_equipment)
        return selected_equipment
    
    def get_selected_inventory_item(self):

        if self.inventory_list.currentItem():

            # inv_item = self.inventory_list.currentItem()                                               ## all has become irrelevant now that I realize I can use the row as an index and compare that to the new "index" list I made when refreshing the inventory
            # inv_item = inv_item.data(2)

            inv_itemid_list = []
            for i in items_inventory.items:
                inv_itemid_list.append(i.itemid)

            inv_list_index = self.inventory_list.currentRow()

            item_id = inv_itemid_list[inv_list_index]

            # i = 0
            # for item in self.inventory_list.findItems("*", Qt.MatchWildcard):                           # i is getting objects
            #     if item.text() == inv_item:
            #         i += 1
            #         inv_index = i - 1
            #         #print(inv_index)

            # inv_item = inv_itemid_list[inv_index]

            #print(inv_item)

            item = Items.Item.get_item_by_id(item_id, inventory=items_inventory)
            #print(items_inventory.items)

            print(item)



            return item
    
    def selection_changed_unit_list(self):

        unit = self.get_selected_unit()
        self.item_stats_label.setText(Unit.display_unit(unit, 3))
        self.refresh_equipment_list()
        self.refresh_inventory_list()
        self.unequip_button.setDisabled(True)


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
            self.item_stats_label.setText(inv_item.display_stats())
            self.unit_equip_list.setCurrentItem(None)
        


        
        
    def equip_equipment(self):
        
        unit = self.get_selected_unit()
        item = self.get_selected_inventory_item()

        equipment_itemid_list = []


        print(item)
        print(unit.name)

        if item.item_type == "weapon":

            if not unit.weaponslot1:
                item.equip(unit, "weaponslot1", items_inventory)
            elif not unit.weaponslot2:
                item.equip(unit, "weaponslot2", items_inventory)
            elif not unit.weaponslot3:
                item.equip(unit, "weaponslot3", items_inventory)
            else:
                inventory_gui.item_stats_label.setText("No Free Weapon Slots!")
                equipment_itemid_list.append(item.itemid)

        elif item.item_type == "armor":

            item.equip(unit, item.slot_type, items_inventory)
            equipment_itemid_list.append(item.itemid)

        self.refresh_inventory_list()
        self.refresh_equipment_list()
        unit_gui.refresh_unit_list()

        self.equip_button.setDisabled(True)
        self.unequip_button.setDisabled(True)

        return equipment_itemid_list


    def unequip_equipment(self):

        unit = self.get_selected_unit()
        item = self.get_selected_equipment()

        item.unequip(unit, item.slot_type, items_inventory)

        print(item.slot_type)

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
    weapon3 = Items.Weapon("Iron Short Sword", 4, 50, "one-handed", "Slashing", 6)
    weapon4 = Items.Weapon("Iron Short Sword", 4, 50, "one-handed", "Slashing", 6)
    items_inventory.items.append(weapon)
    items_inventory.items.append(weapon2)
    items_inventory.items.append(weapon3)
    items_inventory.items.append(weapon4)
    weapon.equip(unittest, "weaponslot3", items_inventory)

    armor = Items.Armor("Iron Mail Armor", 10, "armor", 200, "mail", 10, 10, 10)
    items_inventory.items.append(armor)
    armor.equip(unittest, "armorslot", items_inventory)



    app = QApplication(sys.argv)
    unit_gui = UnitGUI()
    unit_gui.show()
    inventory_gui = InventoryGUI()
    inventory_gui.show()
    sys.exit(app.exec_())