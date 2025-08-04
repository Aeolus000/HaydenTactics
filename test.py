class UI():

    def update_health_bar(self, unit):
        print(f"{unit.name}'s HP is now {unit.hp}!")


class EventSystem():
    def __init__(self):
        self.listeners = {}


    def subscribe(self, event_name, callback):
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(callback)


    def dispatch(self, event_name, **kwargs):
        if event_name in self.listeners:
            for callback in self.listeners[event_name]:
                callback(**kwargs)
        else:
            print("no listeners")


class Unit():
    def __init__(self, name, hp, damage):
        self.name = name
        self.hp = hp
        self.damage = damage


    def apply_attack(self, attacker, defender):
        defender.hp -= attacker.damage
        events.dispatch("unit_damaged", unit=defender)



player = Unit("Player", 50, 25)
goblin = Unit("Goblin", 50, 15)
ui = UI()
events = EventSystem()

events.subscribe("unit_damaged", ui.update_health_bar)

player.apply_attack(player, goblin)
