import Unit
import Items
import Stats
import Models
from Service import *
import Stats
import GUITest2
import Ability
import random




#turn_count = 1
#in_battle = True

unitlist = UnitService.get_all_as_dict()



#print(unitlist)
#print(len(unitlist))


def initiative_tick(unitlist):
    turn = False

    for unit in unitlist:
        if unit["initiative"] >= 100:
            print(f"TURN for {unit["name"]} is up!")
            turn = True
            if unit['is_alive'] == False:
                print(f"{unit["name"]} is Dead, skipping turn.")


    for unit in unitlist:
        if not turn:
            unit["initiative"] = unit["initiative"] + unit["base_spd"]
        
    return sorted(unitlist, reverse=True, key=lambda unit: unit['initiative']), turn

def end_initiative(turn_unit):
        done = False

        if turn_unit["move_points"] == 0 and turn_unit["action_points"] == 0:
            turn_unit["initiative"] = 0
            done = True

        if turn_unit["move_points"] == 1 and turn_unit["action_points"] == 2 and turn_unit["wait"] == True:
            turn_unit["initiative"] = 50
            done = True

        if turn_unit["move_points"] == 1 and turn_unit["action_points"] == 1 and turn_unit["wait"] == True:
            turn_unit["initiative"] = 20
            done = True

        if turn_unit["move_points"] == 1 and turn_unit["action_points"] == 0 and turn_unit["wait"] == True:
            turn_unit["initiative"] = 10
            done = True

        if turn_unit["move_points"] == 0 and turn_unit["action_points"] == 2 and turn_unit["wait"] == True:
            turn_unit["initiative"] = 30
            done = True

        if turn_unit["move_points"] == 0 and turn_unit["action_points"] == 1 and turn_unit["wait"] == True:
            turn_unit["initiative"] = 10
            done = True

        return turn_unit["initiative"], done


def get_base_melee_damage(unit):
     
    melee_damage = (unit["base_str"] / 2) + (unit["base_dex"] / 4)

    return round(melee_damage)

def get_base_melee_defense(unit):
     
    melee_defense = (unit['base_phys_res'])
    return melee_defense

def get_hit_chance(attacker, defender = None, is_ranged = False):

    if not is_ranged:
        if defender:
            finalhitchance = (attacker['melee_hit_chance'])
        else: 
            finalhitchance = attacker['melee_hit_chance']
    elif is_ranged:
        if defender:
            finalhitchance = attacker['ranged_hit_chance']
        else:
            finalhitchance = attacker['ranged_hit_chance']

    if finalhitchance >= 100: finalhitchance = 100

    return round(finalhitchance)

def attack(attacker, defender):

    hit_chance = get_hit_chance(attacker)
    hitroll = random.randint(1, 100)
    hit = False
     
    attacker_damage = get_base_melee_damage(attacker)
    defender_defense = get_base_melee_defense(defender)

    damage = attacker_damage - (attacker_damage * defender_defense / 100) 

    if hitroll >= 100 - hit_chance:
        defender['current_hp'] = defender['current_hp'] - round(damage)
        hit = True
    else:
        hit = False

    if defender['current_hp'] <= 0:
        defender['current_hp'] = 0
        defender['is_alive'] = False

    return hitroll, hit, round(damage)

def separate_teams(init_list):
    team1 = []
    team2 = []
        
    for unit in init_list:
        if unit['team'] == 0:
            team1.append(unit)
        elif unit['team'] >= 1:
            team2.append(unit)

    return team1, team2

def check_victory(init_list):
    team1, team2 = separate_teams(init_list)
    win = bool
    team1dead = 0
    team2dead = 0

    for unit in team1:
        if unit['is_alive'] == False:
            team1dead += 1
    for unit in team2:
        if unit['is_alive'] == False:
            team2dead += 1

    if team2dead >= len(team2):
        win = True
        return win
    if team1dead >= len(team1):
        win = False
        return win

            

