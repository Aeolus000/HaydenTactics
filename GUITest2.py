import sys
import sqlite3
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import Unit
import Stats
import Items
#from Models import Base
from Models import UnitTable, Base
from Service import *

from sqlalchemy import String, select, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


class CharacterCreation(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Character Creation")
        self.setGeometry(500, 500, 200, 200)

        self.character_stats = QLabel()
        self.character_classes = QComboBox(self)
        self.character_name = QLineEdit("Enter Name")
        self.character_name_accept = QPushButton("Finalize")
        #self.character_name_label = QLabel("Enter Character Name:")

        self.reroll_button = QPushButton("Reroll Stats")
        self.cancel_button = QPushButton("Cancel")

        #self.initUI()



    def initUI(self):

        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        self.charclass_index = []
        self.unit_stats = []

        self.setWindowTitle("Character Creation")
        grid = QGridLayout()
        grid2 = QGridLayout()
        hbox = QVBoxLayout()


        grid.addWidget(self.character_name, 0, 0, Qt.AlignLeft)
        self.character_name.setFixedSize(150, 20)
        self.character_name.placeholderText()
        grid.addWidget(self.character_classes, 0, 1, Qt.AlignLeft)
        self.character_classes.setFixedSize(150, 20)
        #grid.addWidget(self.character_name_label, 0, 0)
        grid.addWidget(self.character_stats, 1, 0, Qt.AlignLeft, 2)
        self.character_stats.setMaximumWidth(300)

        grid.addWidget(self.reroll_button, 3, 0, Qt.AlignLeft)

        grid2.addWidget(self.character_name_accept, 0, 0)
        grid2.addWidget(self.cancel_button, 0, 1)


        self.setLayout(hbox)

        hbox.addLayout(grid)
        hbox.addLayout(grid2)
        hbox.addStretch()



        self.display_character_classes()
        self.show()

        self.character_stats.setWordWrap(True)

        self.character_name.selectionChanged.connect(self.text_edited)

        self.reroll_button.pressed.connect(self.display_reroll)

        self.cancel_button.pressed.connect(self.cancel_window)

        self.character_name_accept.pressed.connect(self.finalize)

        self.display_reroll()

    def display_character_classes(self):

        self.character_classes.clear()

        for i in Unit.charclasses:
            self.character_classes.addItem(i)
            self.charclass_index.append(i)


    def text_edited(self):
        self.character_name.clear()


    def display_reroll(self):

        self.unit_stats = Unit.generate_stat_roll()

        self.character_stats.setText(f"""\nStrength:\t\t{self.unit_stats['base_str']}\nDexterity:\t{self.unit_stats['base_dex']}\nSpeed:\t\t{self.unit_stats['base_spd']}\nVitality:\t\t{self.unit_stats['base_vit']}\nConstitution:\t{self.unit_stats['base_con']}\nIntelligence:\t{self.unit_stats['base_int']}\nMind:\t\t{self.unit_stats['base_mnd']}\nResistance:\t{self.unit_stats['base_res']}""")
        return self.unit_stats

    def cancel_window(self):
        self.hide()
        unit_gui.create_character_button.setDisabled(False)
        inventory_gui.show()

    def finalize(self):

        if not self.character_name.displayText():
            self.character_name.setText("Can't be empty!")
        else:
        
            unit_name = self.character_name.text()
            char_class_chosen = self.character_classes.currentIndex()

            char_class = Unit.charclasses[char_class_chosen]

            print(unit_name)
            print(self.unit_stats)
            print(char_class)
            print(char_class_chosen)

            unit = Unit.Unit(unit_name, char_class, 1)

            for key, value in self.unit_stats.items():
                setattr(unit, key, value)

            Unit.unit_list.append(unit)

            unit_gui.refresh_unit_list()
            inventory_gui.refresh_all()

            self.hide()
            self.unit_stats.clear()
            self.character_name.clear()
            self.character_stats.clear()

            unit_gui.create_character_button.setDisabled(False)
            inventory_gui.equip_button.setDisabled(True)
            inventory_gui.unequip_button.setDisabled(True)

            inventory_gui.show()

            return unit


class UnitGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.unit_list = QListWidget(self)
        self.unit_stats_label = QLabel(self)
        self.button = QPushButton("Generate Random Character", self)

        self.level_up_button = QPushButton("Level Up", self)
        self.dismiss_unit_button = QPushButton("Dismiss Unit", self)
        self.message = QLabel(self)

        self.create_character_button = QPushButton("Create Character", self)

        self.initUI()


    def initUI(self):

        self.setWindowTitle("Hayden Tactics")

        grid = QGridLayout()
        grid.addWidget(self.unit_list, 0, 0)
        grid.addWidget(self.button)
        grid.addWidget(self.create_character_button, 2, 0)
        grid.addWidget(self.unit_stats_label, 0, 1)
        #grid.addWidget(self.exit)
        grid.addWidget(self.level_up_button, 1, 1)
        grid.addWidget(self.dismiss_unit_button, 2, 1)
        grid.addWidget(self.message, 0, 2)

        self.unit_list.setGeometry(0, 0, 200, 200)
        self.unit_stats_label.setGeometry(100, 100, 400, 600)

        self.message.setStyleSheet("font-family: calibri; font-size: 20px")

        self.setLayout(grid)

        self.button.clicked.connect(self.display_random_unit)

        self.level_up_button.setDisabled(True)
        self.level_up_button.clicked.connect(self.display_level_up)

        self.unit_list.itemClicked.connect(self.selection_changed)

        self.dismiss_unit_button.setDisabled(True)
        self.dismiss_unit_button.clicked.connect(self.dismiss_unit)

        self.create_character_button.clicked.connect(self.display_created_unit)

        self.refresh_unit_list()

        self.unit_stats_label.setAlignment(Qt.AlignTop)


    def selection_changed(self):

        unit = self.get_selected_unit()

        display_stats = Displays.text_format(unit)

        self.unit_stats_label.setText(display_stats)



        #self.unit_stats_label.setText(unit_stats)

        if self.unit_list.currentItem() == None:
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
        self.unit_list.clear()

        units = UnitService.get_all()
        for unit in units:
            self.unit_list.addItem(f"{unit.id} {unit.name}")

    def get_selected_unit(self):

        selected = self.unit_list.currentRow()

        #db_unit = UnitService.get_attributes_by_id(selected + 1)
        db_unit = UnitService.get_unit_by_row(selected)
        #print(db_unit)

        return db_unit
    

    def display_random_unit(self):

        unit = UnitService.generate_random_unit()

        self.refresh_unit_list()

        self.dismiss_unit_button.setDisabled(True)
        self.level_up_button.setDisabled(True)

    def display_created_unit(self):
        pass

    def display_level_up(self):
        unit = self.get_selected_unit()
        UnitService.level_up(unit)
        UnitService.refresh_stats_noncombat(unit)

        self.selection_changed()
        pass

    def dismiss_unit(self):
        unit = self.get_selected_unit()

        UnitService.dismiss(unit)

        self.unit_list.setCurrentItem(None)
        self.unit_stats_label.clear()
        self.dismiss_unit_button.setDisabled(True)
        self.level_up_button.setDisabled(True)

        self.refresh_unit_list()
        

class InventoryGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Inventory Management")
        self.move(100, 100)


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

        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)

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
        for unit in Unit.unit_list:
            self.unit_list.addItem(f"{unit.unit_id} {unit.name}")

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

        for item in player_inventory.items:
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
        
        return selected_equipment
    
    def get_selected_inventory_item(self):

        if self.inventory_list.currentItem():

            # inv_item = self.inventory_list.currentItem()                                               ## all has become irrelevant now that I realize I can use the row as an index and compare that to the new "index" list I made when refreshing the inventory
            # inv_item = inv_item.data(2)

            inv_itemid_list = []
            for i in player_inventory.items:
                inv_itemid_list.append(i.itemid)

            inv_list_index = self.inventory_list.currentRow()

            item_id = inv_itemid_list[inv_list_index]

            item = Items.Item.get_item_by_id(item_id, inventory=player_inventory)

            print(item)



            return item
    
    def selection_changed_unit_list(self):

        unit = self.get_selected_unit()
        self.item_stats_label.setText(Unit.display_unit(unit, 3))
        self.refresh_equipment_list()
        self.refresh_inventory_list()
        self.unequip_button.setDisabled(True)
        self.equip_button.setDisabled(True)

        self.sync_window_selections()


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

    def sync_window_selections(self):

        selection = self.unit_list.currentRow()

        unit_gui.unit_list.setCurrentRow(selection)
        
        unit = Unit.unit_list[selection]
        stats = Unit.display_unit(unit, 2)

        unit_gui.unit_stats_label.setText(stats)
        
        
    def equip_equipment(self):
        
        unit = self.get_selected_unit()
        item = self.get_selected_inventory_item()

        equipment_itemid_list = []


        #print(item)
        #print(unit.name)

        if item.item_type == "weapon":

            if not unit.weapon_slot1:
                item.equip(unit, "weapon_slot1", player_inventory)
            elif not unit.weapon_slot2:
                item.equip(unit, "weapon_slot2", player_inventory)
            elif not unit.weapon_slot3:
                item.equip(unit, "weapon_slot3", player_inventory)
            else:
                #inventory_gui.item_stats_label.setText("No Free Weapon Slots!")
                equipment_itemid_list.append(item.itemid)

        elif item.item_type == "armor":

            item.equip(unit, item.slot_type, player_inventory)
            equipment_itemid_list.append(item.itemid)

        self.refresh_inventory_list()
        self.refresh_equipment_list()
        self.sync_window_selections()

        self.equip_button.setDisabled(True)
        self.unequip_button.setDisabled(True)



        return equipment_itemid_list


    def unequip_equipment(self):

        unit = self.get_selected_unit()
        item = self.get_selected_equipment()

        item.unequip(unit, item.slot_type, player_inventory)

        print(item.slot_type)

        self.selection_changed_unit_list()
        self.equip_button.setDisabled(True)
        self.unequip_button.setDisabled(True)

        self.refresh_inventory_list()
        self.refresh_equipment_list()
        self.sync_window_selections()


class Displays:

    @staticmethod
    def text_format(unit):
        display_stats = [f'ID: {unit.id}',
            f'Name:\t{unit.name}', 
            f'Job:\t{unit.charclass}',  
            f'Level:\t{unit.level}'
            ]
        display_stats.append(f"\nCurrent / Max HP:\t\t{unit.current_hp} / {unit.max_hp}")
        display_stats.append(f"Current / Max Mana:\t{unit.current_mana} / {unit.max_mana}")
        display_stats.append(f"Strength:\t\t{unit.base_str}")
        display_stats.append(f"Dexterity:\t{unit.base_dex}")
        display_stats.append(f"Speed:\t\t{unit.base_spd}")
        display_stats.append(f"Vitality:\t\t{unit.base_vit}")
        display_stats.append(f"Constitution:\t{unit.base_con}")
        display_stats.append(f"Intelligence:\t{unit.base_int}")
        display_stats.append(f"Mind:\t\t{unit.base_mnd}")
        display_stats.append(f"Resistance:\t{unit.base_res}")
        display_stats.append(f"\nPhysical Damage Reduction:\t{unit.base_phys_res}%")
        display_stats.append(f"Magical Damage Reduction:\t{unit.base_mag_res}%")

        return '\n'.join(display_stats)






if __name__ == '__main__':

    Base.metadata.create_all(engine)

    player_inventory = Items.Inventory(50)

    app = QApplication(sys.argv)
    unit_gui = UnitGUI()
    unit_gui.show()
    #inventory_gui = InventoryGUI()
    #inventory_gui.show()
    #character_creation = CharacterCreation()
    #character_creation.initUI()
    #character_creation.hide()
    sys.exit(app.exec_())