import sys
import sqlite3
from PyQt5 import QtCore
import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui

import Unit
import Stats
import Items
import Combat
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

        self.unit_stats = UnitService.generate_unit_stats()

        self.character_stats.setText(f"""\nStrength:\t\t{self.unit_stats['base_str']}\nDexterity:\t{self.unit_stats['base_dex']}\nSpeed:\t\t{self.unit_stats['base_spd']}\nVitality:\t\t{self.unit_stats['base_vit']}\nConstitution:\t{self.unit_stats['base_con']}\nIntelligence:\t{self.unit_stats['base_int']}\nMind:\t\t{self.unit_stats['base_mnd']}\nResistance:\t{self.unit_stats['base_res']}""")
        return self.unit_stats

    def cancel_window(self):
        self.hide()
        unit_gui.create_character_button.setDisabled(False)
        #inventory_gui.show()

    def finalize(self):

        if not self.character_name.displayText():
            self.character_name.setText("Can't be empty!")
        else:
        
            unit_name = self.character_name.text()
            char_class_chosen = self.character_classes.currentIndex()

            char_class = Unit.charclasses[char_class_chosen]
            #char_class = Unit.CharClassesEnum.name[char_class_chosen]


            unit = UnitService.create(unit_name, char_class, 1, self.unit_stats)

            unit_gui.refresh_unit_list()
            #inventory_gui.refresh_all()

            self.hide()
            self.unit_stats.clear()
            self.character_name.clear()
            self.character_stats.clear()

            unit_gui.create_character_button.setDisabled(False)
            #inventory_gui.equip_button.setDisabled(True)
            #inventory_gui.unequip_button.setDisabled(True)

            #inventory_gui.show()

            return unit

class CombatActions(QWidget):
    def __init__(self):
        super().__init__()

        self.move_button = QPushButton("Move", self)
        self.attack_button = QPushButton("Attack", self)
        self.ability_button = QPushButton("Ability", self)
        self.wait_button = QPushButton("Wait", self)
        self.ability_box = QComboBox(self)

        grid = QVBoxLayout()
        grid.addWidget(self.move_button)
        grid.addWidget(self.attack_button)
        grid.addWidget(self.ability_button)
        grid.addWidget(self.wait_button)
        grid.addWidget(self.ability_box)

        self.setLayout(grid)

        self.ability_button.setDisabled(True)

    def attack_button_pressed(self):
        turn_unit["action_points"] = turn_unit["action_points"] - 1
        #print(f"action points: {turn_unit["action_points"]}")

        if turn_unit["action_points"] == 0:
            self.attack_button.setDisabled(True)

        attacker = turn_unit
        defender = combat_gui.get_selected_unit()
        hitroll, hit, damage = Combat.attack(attacker, defender)

        print(f"{attacker['name']}, roll: {hitroll}, hitchance (low rolls whiff): {Combat.get_hit_chance(attacker, defender)}")
        if hit == True:
            hit = f"Succeeds! {defender['name']} took {damage} damage."
        elif hit == False:
            hit = "Misses!"

        combat_gui.message.setText(f"{turn_unit['name']}'s attack \n{hit}")
        
        combat_gui.target_list_selection_changed()
        #combat_gui.refresh_target_list()

        combat_gui.end_turn_check()

    def move_button_pressed(self):
        turn_unit["move_points"] = turn_unit["move_points"] - 1

        if turn_unit["move_points"] == 0:
            self.move_button.setDisabled(True)

            combat_gui.end_turn_check()

    def wait_button_pressed(self):
        turn_unit["wait"] = True

        combat_gui.end_turn_check()

class CombatGUI(QWidget):

    def __init__(self):
        super().__init__()

        self.turn_list_label = QLabel(self)
        self.turn_list = QTableWidget(self)

        self.target_list_label = QLabel(self)
        self.target_list = QListWidget(self)

        self.turn_unit_stats_label = QLabel(self)
        self.opponent_unit_stats_label = QLabel(self)

        self.turn_unit_combat_stats_label = QLabel(self)
        self.opponent_unit_combat_stats_label = QLabel(self)

        self.message = QLabel(self)
        
        self.combat_actions = CombatActions()

        self.in_battle = True
        self.initUI()

    def initUI(self):
        self.turn_count = 1
        self.unitlist = Combat.create_unitlist()

        i = 0
        for unit in self.unitlist:
            if unit["team"] > 0:
                i += 1
        
        if i == 0:
            UnitService.generate_enemy_team()
            self.unitlist = Combat.create_unitlist()

        self.init_list = self.unitlist
        global in_battle
        global taking_turn
        in_battle = True
        taking_turn = False

        self.setWindowTitle("Combat")

        grid = QGridLayout()
        grid.addWidget(self.turn_list_label, 0, 0)
        grid.addWidget(self.turn_list, 1, 0)

        self.turn_list_label.setText("Turn Order")
        self.turn_list.setColumnCount(2)
        self.turn_list.setRowCount(50)

        grid.addWidget(self.target_list_label, 0, 2)
        grid.addWidget(self.target_list, 1, 2)

        self.target_list_label.setText("Available Targets")

        grid.addWidget(self.turn_unit_stats_label, 3, 0)
        grid.addWidget(self.turn_unit_combat_stats_label, 5, 0)

        self.turn_unit_stats_label.setText("Current Unit Stats")

        grid.addWidget(self.opponent_unit_stats_label, 3, 2)
        grid.addWidget(self.opponent_unit_combat_stats_label, 5, 2)

        self.opponent_unit_stats_label.setText("Opponent Unit Stats")

        grid.addWidget(self.message, 1, 1)

        grid.addWidget(self.combat_actions, 3, 1)

        self.message.setStyleSheet("font-family: calibri; font-size: 16px")

        self.setLayout(grid)

        self.turn_unit_combat_stats_label.setText("Current Unit Combat Stats")
        self.opponent_unit_combat_stats_label.setText("Opponent Unit Combat Stats")

        self.message.setText("Damage Stuff Goes Here")

        self.turn_list.setDisabled(False)
        self.turn_list.setEditTriggers(QAbstractItemView.NoEditTriggers)

        
        self.combat_actions.attack_button.clicked.connect(self.combat_actions.attack_button_pressed)

        self.combat_actions.move_button.clicked.connect(self.combat_actions.move_button_pressed)
        self.combat_actions.wait_button.clicked.connect(self.combat_actions.wait_button_pressed)
        self.target_list.itemClicked.connect(self.target_list_selection_changed)
        self.refresh_turn_order()
        self.run_tick()

    def end_turn_check(self):

        turn_unit["initiative"], end = Combat.end_initiative(turn_unit)

        if end == True:
            if turn_unit['is_alive'] == False:
                turn_unit['death_timer'] += 1
                print(f"{turn_unit['name']} death counters: {turn_unit['death_timer']}")

            Combat.permadeath_check(turn_unit)

            if turn_unit['permadeath'] == True:
                print(f"{turn_unit['name']} has reached 3 death counters, unit permanently lost.")
                self.init_list.remove(turn_unit)
                self.refresh_target_list()
                self.refresh_turn_order()
            self.end_turn()
        elif end == False:
            pass 

    def end_turn(self):

        #print(turn_unit["name"], turn_unit["initiative"])
        global in_battle
        global taking_turn
        in_battle = True
        taking_turn = False

        win = Combat.check_victory(self.init_list)
        if win == None:
            self.run_tick()
        elif win == True:
            self.message.setText("!!!VICTORY!!!")
            self.end_battle()
        elif win == False:
            self.message.setText("!!!DEFEAT!!!")
            self.end_battle()

    def end_battle(self):
        self.combat_actions.move_button.setDisabled(True)
        self.combat_actions.wait_button.setDisabled(True)
        self.combat_actions.attack_button.setDisabled(True)
        self.refresh_target_list()
        self.target_list_selection_changed()
        turn_unit['action_points'] = 0
        turn_unit['move_points'] = 0
        turn_unit['wait'] = True

        UnitService.delete_nonplayer_units()

    def run_tick(self):
        global in_battle
        global taking_turn

        while in_battle == True:

            if taking_turn == False:

                self.init_list, taking_turn = Combat.initiative_tick(unitlist=self.init_list)

                #print(taking_turn)

            if taking_turn == True:
                self.refresh_turn_order()
                in_battle = False
                self.set_turn()

    def set_turn(self):
            
            global turn_unit

            self.target_list.setCurrentItem(None)
            self.opponent_unit_stats_label.setText(None)
            self.opponent_unit_combat_stats_label.setText(None)
            
            self.refresh_target_list()
            self.combat_actions.attack_button.setDisabled(False)
            self.combat_actions.move_button.setDisabled(False)
            self.combat_actions.wait_button.setDisabled(False)

            turn_unit = self.init_list[0]

            Combat.mana_regen(turn_unit)
            
            if turn_unit['is_alive'] == False:
                turn_unit["action_points"] = 0
                turn_unit["move_points"] = 0
                turn_unit["wait"] = False
                self.end_turn_check()
                
            elif turn_unit['is_alive'] == True:
                turn_unit["action_points"] = 2
                turn_unit["move_points"] = 1
                turn_unit["wait"] = False

            self.turn_unit_stats_label.setText(f"""{turn_unit['name']}'s Turn\n\nClass: {turn_unit['charclass']}\n\nStrength:\t\t{turn_unit['base_str']}\nDexterity:\t{turn_unit['base_dex']}\nSpeed:\t\t{turn_unit['base_spd']}\nVitality:\t\t{turn_unit['base_vit']}\nConstitution:\t{turn_unit['base_con']}\nIntelligence:\t{turn_unit['base_int']}\nMind:\t\t{turn_unit['base_mnd']}\nResistance:\t{turn_unit['base_res']}""")
            self.turn_unit_combat_stats_label.setText(f"""\n\nHP:\t\t{turn_unit['current_hp']} / {turn_unit['max_hp']}\nMana:\t\t{turn_unit['current_mana']} / {turn_unit['max_mana']}\n\nBase Melee Damage: {Combat.get_base_melee_damage(turn_unit)}\nBase Phys Resistance: {Combat.get_base_melee_defense(turn_unit)}%""")
        
    def refresh_turn_order(self):

        self.turn_list.clear()

        self.turn_list.setRowCount(len(self.init_list))
        header1 = QTableWidgetItem("Unit")
        header2 = QTableWidgetItem("Initiative")
        self.turn_list.setHorizontalHeaderItem(0, header1)
        self.turn_list.setHorizontalHeaderItem(1, header2)

        row = -1

        for unit in self.init_list:
            blah = QTableWidgetItem(f"{unit["name"]}")
            blah2 = QTableWidgetItem(f"{unit["initiative"]}")
            if unit["team"] > 0:
                blah.setBackground(QtGui.QColor(243, 49, 8))
                blah2.setBackground(QtGui.QColor(243, 49, 8))
            elif unit["team"] == 0:
                blah.setBackground(QtGui.QColor(8, 203, 243))
                blah2.setBackground(QtGui.QColor(8, 203, 243))


            self.turn_list.setItem(row + 1, 0, blah)
            self.turn_list.setItem(row + 1, 1, blah2)
            row += 1

            #self.turn_list.addItem(f"{unit["id"]} {unit["name"]}\t Initiative: {unit["initiative"]}")

        # units = UnitService.get_all()
        # for unit in units:
        #     self.turn_list.addItem(f"{unit.id} {unit.name}\t\t Initiative: {unit.initiative}")


    def get_selected_unit(self):

        selected = self.target_list.currentRow()
        unit = self.init_list[selected]

        return unit
    
    def refresh_target_list(self):
        self.target_list.clear()
        units = self.init_list
        turn_unit = self.init_list[0]

        for unit in units:
            if unit["team"] == turn_unit["team"]:
                if unit['is_alive'] == True:
                    self.target_list.addItem(f"{unit["name"]}")
                else:
                    self.target_list.addItem(f"{unit["name"]} (DOWNED)")
            else:
                if unit['is_alive'] == True:
                    self.target_list.addItem(f"{unit["name"]} (enemy)")
                else:
                    self.target_list.addItem(f"{unit["name"]} (enemy) (DOWNED)")

    def target_list_selection_changed(self):

        selected = self.target_list.currentRow()

        unit1 = self.init_list[selected]

        if unit1['is_alive'] == False:
            self.combat_actions.attack_button.setDisabled(True)
        elif unit1['is_alive'] == True and turn_unit['action_points'] > 0:
            self.combat_actions.attack_button.setDisabled(False)

        #display_stats = Displays.text_format(unit1, 0)

        self.opponent_unit_stats_label.setText(f"""Target: {unit1['name']}\n\nClass: {unit1['charclass']}\n\nStrength:\t\t{unit1['base_str']}\nDexterity:\t{unit1['base_dex']}\nSpeed:\t\t{unit1['base_spd']}\nVitality:\t\t{unit1['base_vit']}\nConstitution:\t{unit1['base_con']}\nIntelligence:\t{unit1['base_int']}\nMind:\t\t{unit1['base_mnd']}\nResistance:\t{unit1['base_res']}""")
        self.opponent_unit_combat_stats_label.setText(f"""\n\nHP:\t\t{unit1['current_hp']} / {unit1['max_hp']}\nMana:\t\t{unit1['current_mana']} / {unit1['max_mana']}\n\nBase Melee Damage: {Combat.get_base_melee_damage(unit1)}\nBase Phys Resistance: {Combat.get_base_melee_defense(unit1)}%""")

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

        self.combat_button = QPushButton("FIGHT!", self)

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
        grid.addWidget(self.combat_button, 0, 3)

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

        self.create_character_button.clicked.connect(self.display_create_unit)

        self.refresh_unit_list()

        self.unit_stats_label.setAlignment(Qt.AlignTop)

        self.combat_button.clicked.connect(self.display_combat)


    def selection_changed(self):
        unit = self.get_selected_unit()
        display_stats = Displays.text_format(unit, 1)
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

        inventory_gui.refresh_all()
        inventory_gui.unequip_button.setDisabled(True)
        inventory_gui.equip_button.setDisabled(True)

        
    def refresh_unit_list(self):
        self.unit_list.clear()

        units = UnitService.get_all()
        for unit in units:
            if unit.team == 0:
                self.unit_list.addItem(f"{unit.id} {unit.name}")

    def get_selected_unit(self):

        selected = self.unit_list.currentRow()
        #db_unit = UnitService.get_attributes_by_id(selected + 1)
        db_unit = UnitService.get_unit_by_row(selected)
        return db_unit
    
    def display_combat(self):
        global combat_gui
        check = UnitService.get_all_as_dict()

        if check == []:
            self.unit_stats_label.setText("You have no Units!")
            print("You have no Units!")
        elif check:
            combat_gui = CombatGUI()
            combat_gui.show()

    def display_random_unit(self):
        unit = UnitService.generate_random_unit()
        self.refresh_unit_list()

        self.dismiss_unit_button.setDisabled(True)
        self.level_up_button.setDisabled(True)

    def display_create_unit(self):
        character_creation.show()
        character_creation.display_reroll()

        self.create_character_button.setDisabled(True)
        #inventory_gui.hide()

    def display_level_up(self):
        unit = self.get_selected_unit()
        UnitService.level_up(unit)
        UnitService.refresh_stats_noncombat(unit)
        self.selection_changed()

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

        #self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)

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

        units = UnitService.get_all()
        for unit in units:
            self.unit_list.addItem(f"{unit.id} {unit.name}")

    def refresh_equipment_list(self):
        pass


    def refresh_inventory_list(self):

        pass

    def refresh_all(self):

        self.refresh_unit_list()
        self.refresh_equipment_list()
        self.refresh_inventory_list()

    def get_selected_unit(self):
        selected = self.unit_list.currentRow()

        db_unit = UnitService.get_unit_by_row(selected)

        return db_unit
    
    def get_selected_equipment(self):

        pass
    
    def get_selected_inventory_item(self):

        pass
    
    def selection_changed_unit_list(self):

        unit = self.get_selected_unit()

        display_stats = Displays.text_format(unit)

        self.item_stats_label.setText(display_stats)
        
        self.sync_window_selections()


    def selection_changed_equipment_list(self):

        if self.unit_equip_list.currentItem() == None:
            self.unequip_button.setDisabled(True)

        else:
            self.unequip_button.setDisabled(False)

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
        db_unit = UnitService.get_unit_by_row(selection)
        
        stats = Displays.text_format(db_unit)

        unit_gui.unit_stats_label.setText(stats)
        
        
    def equip_equipment(self):
         
        pass

    def unequip_equipment(self):

        pass

class Displays:

    @staticmethod
    def text_format(unit, option = 0):
        display_stats = [f'ID: {unit.id}',
            f'Name:\t{unit.name}', 
            f'Job:\t{unit.charclass}',  
            f'Level:\t{unit.level}'
            ]
        display_stats.append(f"\nCurrent / Max HP:\t\t{unit.current_hp} / {unit.max_hp}")
        display_stats.append(f"Current / Max Mana:\t{unit.current_mana} / {unit.max_mana}")
        if option == 1:
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
    inventory_gui = InventoryGUI()
    #inventory_gui.show()
    character_creation = CharacterCreation()
    character_creation.initUI()
    character_creation.hide()

    # combat_gui = CombatGUI()
    # combat_gui.show()

    #WeaponService.populate_weapons()
    sys.exit(app.exec_())