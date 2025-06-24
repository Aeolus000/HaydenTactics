import Combat
import Unit
import GUITest2
import Ability
import Items
import Stats


class StatusEffect():
    def __init__(self, duration, target, tooltip, type):
        self.duration = duration
        self.target = target
        self.tooltip = tooltip
        self.type = type



class StatusEffectPoison(StatusEffect):
    def __init__(self, target):
        self.name = "Poison"
        self.duration = 3
        self.target = target
        self.type = "debuff"
        self.tooltip = "Poisons the target for 3 turns, dealing 10% of their maximum health as damage at the start of their turn."

    def process(self):
        self.duration -= 1
        self.target['current_hp'] = (round(self.target['current_hp'] - (self.target['max_hp'] * 0.1)))
        if self.target['current_hp'] < 0:
            self.target['current_hp'] = 0
            self.target['is_alive'] = False
        print(self.target['name'] + " is afflicted with poison for " + str(self.duration) + " more turns!")

        if self.duration <= 0:
            self.target['status_effects'].remove(self)
            print(self.target['status_effects'])


class StatusEffectWeaken(StatusEffect):
    def __init__(self, target):
        self.name = "Weaken"
        self.duration = 2
        self.target = target
        self.type = "debuff"
        self.tooltip = "Halves the target's Strength for 2 turns."
        self.original_str = target['base_str']

    
    def process(self):
        self.duration -= 1
        print(self.target['name'] + " is affected by Weaken for " + str(self.duration) + " more turns!")
        #self.target['base_str'] = (self.target['base_str'] / 2)

        if self.duration <= 0:
            self.target['base_str'] = self.original_str
            self.target['status_effects'].remove(self)


