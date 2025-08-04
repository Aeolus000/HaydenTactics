import sqlite3
import Unit
import Items
import Stats
import Combat
from StatusEffects import *

class Ability:
    def __init__(self, name, charclass, mana_cost, hp_cost, action_cost, target_type, area_effect, damage, damage_element):
        
        self.name = name                            # Ability Name
        self.charclass = charclass                  # Which charclass the ability will belong to
        self.mana_cost = mana_cost                  # How much mana it costs
        self.hp_cost = hp_cost                      # How much hp it costs (if any, primarily for hemomancer abilities)
        self.action_cost = action_cost              # How many action points will it cost to cast
        self.targeting = target_type                # Will you target a unit or an area? (aka a square on the map)
        self.area_effect = area_effect              # How big is the area this will hit? for instance, 3 = 3 tiles from center
        self.damage = damage                        # How much damage will this do? Negative values can heal.
        self.damage_element = damage_element        # What element is this? (May have elemental resistances later on)


#heal = Ability("Heal", "Priest", 10, 0, 1, "single", 1, -10, "Holy")

    def add_to_unit(self, unit):
        unit['abilities'].append(self)


class Poison(Ability):
    def __init__(self):
        #super().__init__()
        self.name = "Poison"
        self.mana_cost = 2
        self.action_cost = 1
        self.type = "debuff"

    def apply(self, target, caster = None):
        for i in target['status_effects']:
            if i.name == "Poison":
                target['status_effects'].remove(i)

        target['status_effects'].append(StatusEffectPoison(target))

class Weaken(Ability):
    def __init__(self):
        self.name = "Weaken"
        self.mana_cost = 5
        self.action_cost = 1
        self.type = "debuff"
        self.stack = 1
        self.original_strength = 0

    def apply(self, target, caster = None):
        target['base_str'] = round((target['base_str'] / 2))
        print("current strength: " + str(target['base_str']))

        target['status_effects'].append(StatusEffectWeaken(target))        

class Heal(Ability):
    def __init__(self):
        self.name = "Heal"
        self.mana_cost = 10
        self.action_cost = 2
        self.type = "buff"

    def apply(self, target, caster, just_data = False):

        if just_data:
            heal_amount = round(((target['max_hp'] * 0.2) + (caster['base_int'] * 2)))
            return heal_amount
        
        target['current_hp'] = target['current_hp'] + round(((target['max_hp'] * 0.2) + (caster['base_int'] * 2)))
        if target['current_hp'] > target['max_hp']:
            target['current_hp'] = target['max_hp']

class Fireball(Ability):
    def __init__(self):
        self.name = "Fireball"
        self.mana_cost = 20
        self.action_cost = 2
        self.type = "area"

    def apply(self, target, caster, just_data = False):
        pass
