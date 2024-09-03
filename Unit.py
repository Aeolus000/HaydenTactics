import random
import Stats
import Items

nameslist = ["Aeolus", "Abraxis", "Zeyta", "Zalzaide", "Armagus", "Ibane", "Gen'jin", "Byron", "Jaeremy", "Artemisia", "Judica", "Adalinde", "Olivia", "Garth", "Erebus", "Marius", "Daniel", "Selene", "Liam"]
charclasses = ["Weaponmaster", "Shaman", "Necromancer", "Monk", "Demonologist", "Elementalist", "Rogue", "Hemomancer", "Astromancer", "Crusader", "Priest"]
unitlist = []

class Unit:

    lastknownid = 0

    def __init__(self, name, charclass, level):
        self.name = name
        self.charclass = charclass
        self.level = level



        # base stat roll
        self.baseStrength = 10 + random.randrange(-2, 2)
        self.baseDexterity = 10 + random.randrange(-2, 2)
        self.baseSpeed = 10 + random.randrange(-2, 2)
        self.baseVitality = 10 + random.randrange(-2, 2)
        self.baseConstitution = 10 + random.randrange(-2, 2)
        self.baseIntelligence = 10 + random.randrange(-2, 2)
        self.baseMind = 10 + random.randrange(-2, 2)
        self.baseResistance = 10 + random.randrange(-2, 2)

        self.maxHP = 50 + (4 * self.baseVitality)
        self.currentHP = self.maxHP

        self.maxMana = 20 + (self.baseMind)
        self.currentMana = self.maxMana

        self.melee_hit_chance = round((70 + (0.25 * self.baseDexterity)))
        self.ranged_hit_chance = 50 + (0.25 * self.baseDexterity)

        self.basePhysicalResistance = (self.baseConstitution * 0.5)
        self.baseMagicalResistance = (self.baseResistance * 0.5)

        self.baseEvasion = 0
        self.baseBlockChance = 0

        Unit.lastknownid += 1
        self.id = Unit.lastknownid
        

        self.weaponslot1 = None
        self.weaponslot2 = None


def get_unit_by_id(id):
    for unit in unitlist:
        if id == unit.id:
            return unit

def melee_damage(unit):
    weapon_damage = 0
    if unit.weaponslot1:
        weapon_damage = unit.weaponslot1.damagerange
    melee_damage = (unit.baseStrength) + (unit.baseDexterity / 2) + weapon_damage
    return round(melee_damage)

def display_unit(unit, option = 0):
    print("\n************************\n")
    print(f"ID: {unit.id}\tName:\t{unit.name}")
    print(f"Job:\t{unit.charclass}")
    print(f"Level:\t{unit.level}")

    if option == 1:
        print(f"HP: {unit.currentHP}/{unit.maxHP} Mana: {unit.currentMana}/{unit.maxMana}")

    if option == 2:  
        print("************************")
        print(f"Current / Max HP:\t{unit.currentHP} / {unit.maxHP}")
        print(f"Current / Max Mana:\t{unit.currentMana} / {unit.maxMana}")
        print(f"Strength:\t{unit.baseStrength}")
        print(f"Dexterity:\t{unit.baseDexterity}")
        print(f"Speed:\t\t{unit.baseSpeed}")
        print(f"Vitality:\t{unit.baseVitality}")
        print(f"Constitution:\t{unit.baseConstitution}")
        print(f"Intelligence:\t{unit.baseIntelligence}")
        print(f"Mind:\t\t{unit.baseMind}")
        print(f"Resistance:\t{unit.baseResistance}")
        print(f"You would deal {melee_damage(unit)} melee damage.")
        print(f"You have a {unit.melee_hit_chance}% chance to hit.")
        print(f"You have {unit.basePhysicalResistance}% Physical Resistance.")
        if unit.weaponslot1:
            print(f"You have a {unit.weaponslot1.name} equipped.")
    
def level_up(unit):
   
    stats = Stats.levelup_stats[unit.charclass]

    for key, value in stats.as_dict().items():
        unit_current_stat = getattr(unit, key)
        setattr(unit, key, unit_current_stat + value)

        #print(f"{key, value}")

    unit.level += 1
    refresh_stats(unit)

    print(f"{unit.name} leveled up to Level {unit.level}!")
        #unit.baseStrength = unit.baseStrength + stat['str']

def refresh_stats(unit):

    unit.maxHP = 50 + (4 * unit.baseVitality)
    #unit.currentHP = unit.maxHP

    unit.maxMana = 20 + (unit.baseMind)
    #unit.currentMana = unit.maxMana

    unit.melee_hit_chance = 70 + (0.25 * unit.baseDexterity)
    unit.ranged_hit_chance = 50 + (0.25 * unit.baseDexterity)

    unit.basePhysicalResistance = (unit.baseConstitution * 0.5)
    unit.baseMagicalResistance = (unit.baseResistance * 0.5)

    unit.baseEvasion = 0
    unit.baseBlockChance = 0



def attack(attacker, opponent):
    #attackerHitChance = attacker.melee_hit_chance
    #opponentEvasion = opponent.baseEvasion

    finalhitchance = (attacker.melee_hit_chance - opponent.baseEvasion)

    hitroll = random.randint(1, 100)

    print(f"You have a {finalhitchance}% chance to hit.")

    if hitroll >= 100 - finalhitchance:
        print(f"Roll: {hitroll}")
        print(f"{attacker.name} HIT for {melee_damage(attacker)} damage!")

        opponent.currentHP = opponent.currentHP - melee_damage(attacker)
        print(f"{opponent.name} now has {opponent.currentHP} of {opponent.maxHP} HP.")
    else:
        print(hitroll)
        print(f"{attacker.name} missed.")

def generate_random_unit():
    randomname = random.choices(nameslist)[0]
    charclass = random.choices(charclasses)[0]

#    validname = False

#    if validname == False:
#        for unit in unitlist:
#            if randomname == unit.name:
#                randomname = random.choices(names)
#                print(f"{randomname} already taken.")
#            else:
#                print(f"{randomname}")
#                validname = True

    randomunit = Unit(randomname, charclass, 1)
    unitlist.append(randomunit)
    return randomunit



#display_unit(unit1)
#random_unit()
#random_unit()








