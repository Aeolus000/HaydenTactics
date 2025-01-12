import Unit
import Stats
import Models
import Service
import Combat
import Ability
import Items
import GUITest2
import json


# unit = Unit.generate_random_unit() 
# unit.is_alive = True

# unit.weapon_slot1 = ["blah", 1, 5, "blahblah"]

# testlist = []
# testlist.append(unit.__dict__)

# print(unit.__dict__)


# with open('test2.json', 'w') as blah:
#     json.dump(unit.__dict__, blah, indent=1)


testlist = Combat.create_unitlist()

with open('test.json', 'w') as blah:
    json.dump(testlist, blah, indent=1)

with open('test.json', 'r') as blah:
    testlist2 = json.load(blah)


print(testlist2)