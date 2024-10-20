import Unit
import Items
import Stats
import Models
from Service import *
import Stats
import GUITest2
import Ability




#turn_count = 1
#in_battle = True

unitlist = UnitService.get_all_as_dict()



#print(unitlist)
#print(len(unitlist))


def initiative_tick(unitlist):
    for unit in unitlist:
        unit["initiative"] = unit["initiative"] + unit["base_spd"]

        #unitlist.sort(reverse = True, key = unit["initiative"])

        #print(unit["name"], unit["initiative"])

        if unit["initiative"] >= 100:
            print(f"TURN for {unit["name"]} is up!")

            unit["initiative"] = 0
            break
        
    return sorted(unitlist, reverse=True, key=lambda unit: unit['initiative'])







action_points = 2
move_point = 1
wait = False

if move_point == 0 and action_points == 0:
    unit["initiative"] = 0

if move_point == 1 and action_points == 2 and wait == True:
    unit["initiative"] = 50

if move_point == 1 and action_points == 1 and wait == True:
    unit["initiative"] = 20

if move_point == 1 and action_points == 0 and wait == True:
    unit["initiative"] = 10

if move_point == 0 and action_points == 2 and wait == True:
    unit["initiative"] = 30

if move_point == 0 and action_points == 1 and wait == True:
    unit["initiative"] = 10




