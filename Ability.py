import sqlite3
import Unit
import Items
import Stats
import Combat
import StatusEffects


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


#Heal = Ability("Heal", "Priest", 10, 0, 1, "single", 1, -10, "Holy")




class Poison(Ability):
    def __init__(self):
        #super().__init__()
        self.name = "Poison"
        self.mana_cost = 2
        self.action_cost = 1

    def add_to_unit(self, unit):
        unit['abilities'].append(self)

    def apply(target):
        target['status_effects'].append(StatusEffects.StatusEffectPoison(target))

class Weaken(Ability):
    def __init__(self):
        self.name = "Weaken"
        self.mana_cost = 5
        self.action_cost = 1

    def apply(target):
        target['status_effects'].append(StatusEffects.StatusEffectWeaken(target))
        target['base_str'] = round((target['base_str'] / 2))