#######                                                                                     #######
#######                                                                                     #######
#######                                                                                     #######
#######                                                                                     #######
#######                                                                                     #######
#######     This file is no longer really used, but it has a lot of the groundwork          #######
#######     of the rules and numbers I used, so I keep it on the side to keep myself        #######
#######     consistent and organized. Check Combat.py and Models/Services                   #######




import sqlite3

import random
import Stats
import Items
import Models

from enum import Enum

nameslist = ["Aeolus", "Abraxis", "Zeyta", "Zalzaide", "Armagus", "Ibane", "Gen'jin", "Byron", "Jaeremy", "Artemisia", "Judica", 
             "Adalinde", "Olivia", "Garth", "Erebus", "Marius", "Daniel", "Selene", "Liam", "Hayden", "Jessica", "Kayloc", 
             "Tetsedah", "Soultrax", "Tsoul", "Anathros", "Sathson", "Brody", "Cameron", "Brock", "Kevin", "Alessandro", 
             "Madeline", "Thomas", "Delwin Praeg", "Ryan", "Justin", "McCray", "Chase", "Elyse", "Noah", "Stephen", "Carlton", "Honeyglow", "Austyn"]
charclasses = ["Weaponmaster", "Shaman", "Necromancer", "Monk", "Demonologist", "Elementalist", "Rogue", "Hemomancer", "Astromancer", "Crusader", "Priest"]

# CharClassesEnum
#     Weaponmaster = 1
#     Shaman = 2
#     Necromancer = 3
#     Monk = 4
#     Demonologist = 5
#     Elementalist = 6
#     Rogue = 7
#     Hemomancer = 8
#     Astromancer = 9
#     Crusader = 10
#     Priest = 11


enemycharclasses = ["Goon", "Gob", "Skeleton"]

unit_list = []
enemy_unit_list = []

class Unit:

    lastknownid = 0

    def __init__(self, name, charclass, level):
        self.name = name
        self.charclass = charclass
        self.level = level

        self.exp = 0
        self.is_alive = bool
        self.action_points = 0

        # base stat roll
        self.base_str = 10 + random.randrange(-2, 3)
        self.base_dex = 10 + random.randrange(-2, 3)
        self.base_spd = 10 + random.randrange(-2, 3)
        self.base_vit = 10 + random.randrange(-2, 3)
        self.base_con = 10 + random.randrange(-2, 3)
        self.base_int = 10 + random.randrange(-2, 3)
        self.base_mnd = 10 + random.randrange(-2, 3)
        self.base_res = 10 + random.randrange(-2, 3)

        self.max_hp = 75 + (4 * self.base_vit)
        self.current_hp = self.max_hp

        self.max_mana = 10 + (2 * self.base_mnd)
        self.current_mana = self.max_mana

        self.melee_hit_chance = 70 + (self.base_dex / 5)
        self.ranged_hit_chance = 50 + (self.base_dex / 4)

        self.base_phys_res = (self.base_con * 0.5)
        self.base_mag_res = (self.base_res * 0.5)

        self.base_evasion = 0

        self.initiative = 0

        Unit.lastknownid += 1
        self.unit_id = Unit.lastknownid

        self.weapon_slot1 = None
        self.weapon_slot2 = None
        self.weapon_slot3 = None

        self.helmet_slot = None
        self.armor_slot = None
        self.leg_slot = None
        self.ring_slot = None

    def get_equipment_as_dict(self):

        return {
                        'weapon_slot1': self.weapon_slot1,
                        'weapon_slot2': self.weapon_slot2,
                        'weapon_slot3': self.weapon_slot3,
                        'helmet_slot': self.helmet_slot,
                        'armor_slot': self.armor_slot,
                        'leg_slot': self.leg_slot,
                        'ring_slot': self.ring_slot,
                            }
    
    def get_damage_reduction(self):
        damage_reduction = (self.base_phys_res / 100)
        return damage_reduction
    
    def get_melee_damage(self):
        weapon_damage = 0
        if self.weapon_slot1:
            weapon_damage = self.weapon_slot1.damagerange
        melee_damage = (self.base_str / 2) + (self.base_dex / 4) + weapon_damage 
        return round(melee_damage)
    
    def refresh_stats(self):

        self.max_hp = 75 + (4 * self.base_vit)
        self.current_hp = self.max_hp

        self.max_mana = 10 + (2 * self.base_mnd)
        self.current_mana = self.max_mana

        self.melee_hit_chance = 70 + (self.base_dex / 5)
        self.ranged_hit_chance = 50 + (self.base_dex / 4)

        self.base_phys_res = (self.base_con * 0.5)
        self.base_mag_res = (self.base_res * 0.5)

        self.base_evasion = 0
        self.baseBlockChance = 0



def get_unit_by_id(id):
    for unit in unit_list:
        if id == unit.unit_id:
            return unit
        
def generate_stat_roll():

    return {
    'base_str': 10 + random.randrange(-2, 3),
    'base_dex': 10 + random.randrange(-2, 3),
    'base_spd': 10 + random.randrange(-2, 3), 
    'base_vit': 10 + random.randrange(-2, 3),
    'base_con': 10 + random.randrange(-2, 3),
    'base_int': 10 + random.randrange(-2, 3),
    'base_mnd': 10 + random.randrange(-2, 3),
    'base_res': 10 + random.randrange(-2, 3),
    }
    


def damage_calc(attacker, opponent):

    finaldamage = attacker.get_melee_damage - (attacker.get_melee_damage() * opponent.get_damage_reduction())
    return round(finaldamage)

def display_unit(unit, option = 0):
    display_stats = [f'ID: {unit.unit_id}',
                    f'Name:\t{unit.name}', 
                    f'Job:\t{unit.charclass}',  
                    f'Level:\t{unit.level}'
                    ]
    if option == 1:
        display_stats.append(f'\nHP: {unit.current_hp}/{unit.max_hp}   Mana: {unit.current_mana}/{unit.max_mana}')
        if unit.weapon_slot1: display_stats.append(f'\nEQUIP: {unit.weapon_slot1.name}')
        if unit.weapon_slot2: display_stats.append(f'EQUIP: {unit.weapon_slot2.name}')
        if unit.weapon_slot3: display_stats.append(f'EQUIP: {unit.weapon_slot3.name}')

    if option == 2:
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
        display_stats.append(f"\nMelee Damage:\t{unit.get_melee_damage()}")
        display_stats.append(f"Melee Hit Chance:\t{(get_hit_chance(unit, None, False))}%")
        display_stats.append(f"Ranged Hit Chance:{(get_hit_chance(unit, None, True))}%")
        display_stats.append(f"\nPhysical Damage Reduction:\t{unit.base_phys_res}%")
        display_stats.append(f"Magical Damage Reduction:\t{unit.base_mag_res}%")
        if unit.weapon_slot1: display_stats.append(f'\nEQUIP: {unit.weapon_slot1.name}')
        if unit.weapon_slot2: display_stats.append(f'EQUIP: {unit.weapon_slot2.name}')
        if unit.weapon_slot3: display_stats.append(f'EQUIP: {unit.weapon_slot3.name}')

    if option == 3:
        display_stats.append(f'\n')
        if unit.weapon_slot1: display_stats.append(f'Weapon Slot 1: {unit.weapon_slot1.name}')
        if unit.weapon_slot2: display_stats.append(f'Weapon Slot 2: {unit.weapon_slot2.name}')
        if unit.weapon_slot3: display_stats.append(f'Weapon Slot 3: {unit.weapon_slot3.name}')
            


    return '\n'.join(display_stats)
    
    
def level_up(unit):
   
    stats = Stats.levelup_stats[unit.charclass]

    for key, value in stats.as_dict().items():
        unit_current_stat = getattr(unit, key)
        setattr(unit, key, unit_current_stat + value)

    unit.level += 1
    unit.refresh_stats()

    #print(f"{unit.name} leveled up to Level {unit.level}!")



def get_hit_chance(attacker, opponent = None, is_ranged = False):

    if not is_ranged:
        if opponent:
            finalhitchance = (attacker.melee_hit_chance - opponent.base_evasion)
        else: 
            finalhitchance = attacker.melee_hit_chance
    elif is_ranged:
        if opponent:
            finalhitchance = (attacker.ranged_hit_chance - opponent.base_evasion)
        else:
            finalhitchance = attacker.ranged_hit_chance

    if finalhitchance >= 100: finalhitchance = 100

    return round(finalhitchance)


def attack(attacker, opponent):
    #attackerHitChance = attacker.melee_hit_chance
    #opponentEvasion = opponent.base_evasion

    hitchance = get_hit_chance(attacker, opponent)

    hitroll = random.randint(1, 100)

    print(f"You have a {hitchance}% chance to hit.")

    if hitroll >= 100 - hitchance:
        print(f"Roll: {hitroll}")
        print(f"{attacker.name} HIT for {damage_calc(attacker, opponent)} damage!")

        opponent.current_hp = opponent.current_hp - damage_calc(attacker, opponent)
        print(f"{opponent.name} now has {opponent.current_hp} of {opponent.max_hp} HP.")
    else:
        print(hitroll)
        print(f"{attacker.name} missed.")

def generate_random_unit():

    if len(nameslist) <= 0:
        #randomname = "Out Of Names"
        nameslist.extend(["Aeolus", "Abraxis", "Zeyta", "Zalzaide", "Armagus", "Ibane", "Gen'jin", "Byron", "Jaeremy", "Artemisia", "Judica", 
             "Adalinde", "Olivia", "Garth", "Erebus", "Marius", "Daniel", "Selene", "Liam", "Hayden", "Jessica", "Kayloc", 
             "Tetsedah", "Soultrax", "Tsoul", "Anathros", "Sathson", "Brody", "Cameron", "Brock", "Kevin", "Alessandro", 
             "Madeline", "Thomas", "Delwin Praeg", "Ryan", "Justin", "McCray", "Chase", "Elyse", "Noah", "Stephen", "Carlton", "Honeyglow", "Austyn"])

    randomname = random.choice(nameslist)
    nameslist.remove(randomname)

    charclass = random.choice(charclasses)


    #Service.UnitService.create("Hayden", "Shaman", 1)
    randomunit = Unit(randomname, charclass, 1)
    unit_list.append(randomunit)
    return randomunit

