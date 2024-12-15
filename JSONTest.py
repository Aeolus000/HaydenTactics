import Unit
import Stats
import Models
import Service
import Combat
import Ability
import Items
import GUITest2
import json




testlist = Combat.create_unitlist()

with open('test.json', 'w') as blah:
    json.dump(testlist, blah, indent=1)

with open('test.json', 'r') as blah:
    testlist2 = json.load(blah)


#print(testlist2)