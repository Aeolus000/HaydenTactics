import random
import Stats
import Items

nameslist = ["Aeolus", "Abraxis", "Zeyta", "Zalzaide", "Armagus", "Ibane", "Gen'jin", "Byron", "Jaeremy", "Artemisia", "Judica", "Adalinde", "Olivia", "Garth", "Erebus", "Marius", "Daniel", "Selene", "Liam", "Hayden", "Jessica", "Kayloc", "Tetsedah", "Soultrax", "Tsoul", "Anathros", "Sathson"]
charclasses = ["Weaponmaster", "Shaman", "Necromancer", "Monk", "Demonologist", "Elementalist", "Rogue", "Hemomancer", "Astromancer", "Crusader", "Priest"]
unitlist = []
enemyunitlist = []

class Unit:

    lastknownid = 0

    def __init__(self, name, charclass, level):
        self.name = name
        self.charclass = charclass
        self.level = level



        # base stat roll
        self.baseStrength = 10 + random.randrange(-2, 3)
        self.baseDexterity = 10 + random.randrange(-2, 3)
        self.baseSpeed = 10 + random.randrange(-2, 3)
        self.baseVitality = 10 + random.randrange(-2, 3)
        self.baseConstitution = 10 + random.randrange(-2, 3)
        self.baseIntelligence = 10 + random.randrange(-2, 3)
        self.baseMind = 10 + random.randrange(-2, 3)
        self.baseResistance = 10 + random.randrange(-2, 3)

        self.maxHP = 75 + (4 * self.baseVitality)
        self.currentHP = self.maxHP

        self.maxMana = 10 + (2 * self.baseMind)
        self.currentMana = self.maxMana

        self.melee_hit_chance = 70 + (self.baseDexterity / 5)
        self.ranged_hit_chance = 50 + (self.baseDexterity / 4)

        self.basePhysicalResistance = (self.baseConstitution * 0.5)
        self.baseMagicalResistance = (self.baseResistance * 0.5)

        self.baseEvasion = 0
        self.baseBlockChance = 0

        Unit.lastknownid += 1
        self.id = Unit.lastknownid
        

        self.weaponslot1 = None
        self.weaponslot2 = None
        self.weaponslot3 = None

        self.helmetslot = None
        self.armorslot = None
        self.legslot = None
        self.ringslot = None

    def get_equipment_as_dict(self):

        return {
                        'weaponslot1': self.weaponslot1,
                        'weaponslot2': self.weaponslot2,
                        'weaponslot3': self.weaponslot3,
                        'helmetslot': self.helmetslot,
                        'armorslot': self.armorslot,
                        'legslot': self.legslot,
                        'ringslot': self.ringslot,
                            }
    
    def get_damage_reduction(self):
        damage_reduction = (self.basePhysicalResistance / 100)
        return damage_reduction
    
    def get_melee_damage(self):
        weapon_damage = 0
        if self.weaponslot1:
            weapon_damage = self.weaponslot1.damagerange
        melee_damage = (self.baseStrength / 2) + (self.baseDexterity / 4) + weapon_damage 
        return round(melee_damage)
    
    def refresh_stats(self):

        self.maxHP = 75 + (4 * self.baseVitality)
        self.currentHP = self.maxHP

        self.maxMana = 10 + (2 * self.baseMind)
        self.currentMana = self.maxMana

        self.melee_hit_chance = 70 + (self.baseDexterity / 5)
        self.ranged_hit_chance = 50 + (self.baseDexterity / 4)

        self.basePhysicalResistance = (self.baseConstitution * 0.5)
        self.baseMagicalResistance = (self.baseResistance * 0.5)

        self.baseEvasion = 0
        self.baseBlockChance = 0



def get_unit_by_id(id):
    for unit in unitlist:
        if id == unit.id:
            return unit





def damage_calc(attacker, opponent):

    finaldamage = attacker.get_melee_damage - (attacker.get_melee_damage() * opponent.get_damage_reduction())
    return round(finaldamage)

def display_unit(unit, option = 0):
    display_stats = [f'ID: {unit.id}',
                    f'Name:\t{unit.name}', 
                    f'Job:\t{unit.charclass}',  
                    f'Level:\t{unit.level}'
                    ]
    if option == 1:
        display_stats.append(f'\nHP: {unit.currentHP}/{unit.maxHP}   Mana: {unit.currentMana}/{unit.maxMana}')
        if unit.weaponslot1: display_stats.append(f'\nEQUIP: {unit.weaponslot1.name}')
        if unit.weaponslot2: display_stats.append(f'EQUIP: {unit.weaponslot2.name}')
        if unit.weaponslot3: display_stats.append(f'EQUIP: {unit.weaponslot3.name}')

    if option == 2:
        display_stats.append(f"\nCurrent / Max HP:\t\t{unit.currentHP} / {unit.maxHP}")
        display_stats.append(f"Current / Max Mana:\t{unit.currentMana} / {unit.maxMana}")
        display_stats.append(f"Strength:\t\t{unit.baseStrength}")
        display_stats.append(f"Dexterity:\t{unit.baseDexterity}")
        display_stats.append(f"Speed:\t\t{unit.baseSpeed}")
        display_stats.append(f"Vitality:\t\t{unit.baseVitality}")
        display_stats.append(f"Constitution:\t{unit.baseConstitution}")
        display_stats.append(f"Intelligence:\t{unit.baseIntelligence}")
        display_stats.append(f"Mind:\t\t{unit.baseMind}")
        display_stats.append(f"Resistance:\t{unit.baseResistance}")
        display_stats.append(f"\nMelee Damage:\t{unit.get_melee_damage()}")
        display_stats.append(f"Melee Hit Chance:\t{(get_hit_chance(unit, None, False))}%")
        display_stats.append(f"Ranged Hit Chance:{(get_hit_chance(unit, None, True))}%")
        display_stats.append(f"\nPhysical Damage Reduction:\t{unit.basePhysicalResistance}%")
        display_stats.append(f"Magical Damage Reduction:\t{unit.baseMagicalResistance}%")
        if unit.weaponslot1: display_stats.append(f'\nEQUIP: {unit.weaponslot1.name}')
        if unit.weaponslot2: display_stats.append(f'EQUIP: {unit.weaponslot2.name}')
        if unit.weaponslot3: display_stats.append(f'EQUIP: {unit.weaponslot3.name}')

    if option == 3:
        display_stats.append(f'\n')
        if unit.weaponslot1: display_stats.append(f'Weapon Slot 1: {unit.weaponslot1.name}')
        if unit.weaponslot2: display_stats.append(f'Weapon Slot 2: {unit.weaponslot2.name}')
        if unit.weaponslot3: display_stats.append(f'Weapon Slot 3: {unit.weaponslot3.name}')
            


    return '\n'.join(display_stats)
    
    
def level_up(unit):
   
    stats = Stats.levelup_stats[unit.charclass]

    for key, value in stats.as_dict().items():
        unit_current_stat = getattr(unit, key)
        setattr(unit, key, unit_current_stat + value)

    unit.level += 1
    unit.refresh_stats()

    #print(f"{unit.name} leveled up to Level {unit.level}!")



def get_hit_chance(attacker, opponent = None, is_ranged = False):

    if not is_ranged:
        if opponent:
            finalhitchance = (attacker.melee_hit_chance - opponent.baseEvasion)
        else: 
            finalhitchance = attacker.melee_hit_chance
    elif is_ranged:
        if opponent:
            finalhitchance = (attacker.ranged_hit_chance - opponent.baseEvasion)
        else:
            finalhitchance = attacker.ranged_hit_chance

    if finalhitchance >= 100: finalhitchance = 100

    return round(finalhitchance)


def attack(attacker, opponent):
    #attackerHitChance = attacker.melee_hit_chance
    #opponentEvasion = opponent.baseEvasion

    hitchance = get_hit_chance(attacker, opponent)

    hitroll = random.randint(1, 100)

    print(f"You have a {hitchance}% chance to hit.")

    if hitroll >= 100 - hitchance:
        print(f"Roll: {hitroll}")
        print(f"{attacker.name} HIT for {damage_calc(attacker, opponent)} damage!")

        opponent.currentHP = opponent.currentHP - damage_calc(attacker, opponent)
        print(f"{opponent.name} now has {opponent.currentHP} of {opponent.maxHP} HP.")
    else:
        print(hitroll)
        print(f"{attacker.name} missed.")

def generate_random_unit():

    if len(nameslist) <= 0:
        #randomname = "Out Of Names"
        nameslist.extend(["Aeolus", "Abraxis", "Zeyta", "Zalzaide", "Armagus", "Ibane", "Gen'jin", "Byron", "Jaeremy", "Artemisia", "Judica", "Adalinde", "Olivia", "Garth", "Erebus", "Marius", "Daniel", "Selene", "Liam", "Hayden", "Jessica", "Kayloc", "Tetsedah", "Soultrax", "Tsoul", "Anathros", "Sathson"])

    randomname = random.choice(nameslist)
    nameslist.remove(randomname)

    charclass = random.choice(charclasses)

    randomunit = Unit(randomname, charclass, 1)
    unitlist.append(randomunit)
    return randomunit








