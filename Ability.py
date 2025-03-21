import sqlite3
import Unit
import Items
import Stats


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


Heal = Ability("Heal", "Priest", 10, 0, 1, "single", 1, -10, "Holy")







def heal(caster, target):

    caster['current_mana'] = caster['current_mana'] - 10
    caster['action_points'] = caster['action_points'] - 1
    target['current_hp'] = target['current_hp'] + 10