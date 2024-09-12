    



levelup_stats = {

    'Weaponmaster': {
        'baseStrength': 4,
        'baseDexterity': 2, 
        'baseSpeed': 1,
        'baseVitality': 4,
        'baseConsistution': 2,
        'baseIntelligence': 0,
        'baseMind': 1,
        'baseResistance': 0,
                    },

    'Elementalist': {
        'baseStrength': 0,
        'baseDexterity': 1, 
        'baseSpeed': 1,
        'baseVitality': 2,
        'baseConsistution': 1,
        'baseIntelligence': 5,
        'baseMind': 3,
        'baseResistance': 2,
                    },

    'Rogue': {
        'baseStrength': 1,
        'baseDexterity': 4, 
        'baseSpeed': 2,
        'baseVitality': 2,
        'baseConsistution': 2,
        'baseIntelligence': 1,
        'baseMind': 2,
        'baseResistance': 2,
                    },
                }                    




# def display_unit(unit, option = 0):
#     print("\n************************\n")
#     print(f"ID: {unit.id}\tName:\t{unit.name}")
#     print(f"Job:\t{unit.charclass}")
#     print(f"Level:\t{unit.level}")

#     if option == 1:
#         print(f"HP: {unit.currentHP}/{unit.maxHP} Mana: {unit.currentMana}/{unit.maxMana}")
#         if unit.weaponslot1:
#             print(f"EQUIP: {unit.weaponslot1.name}")
#             print("\n************************")
#         if unit.weaponslot2:
#             print(f"EQUIP: {unit.weaponslot2.name}")
#             print("\n************************")
#         if unit.weaponslot3:
#             print(f"EQUIP: {unit.weaponslot3.name}")
#             print("\n************************")
              
#     if option == 2:  
#         print("************************")
#         print(f"Current / Max HP:\t{unit.currentHP} / {unit.maxHP}")
#         print(f"Current / Max Mana:\t{unit.currentMana} / {unit.maxMana}")
#         print(f"Strength:\t{unit.baseStrength}")
#         print(f"Dexterity:\t{unit.baseDexterity}")
#         print(f"Speed:\t\t{unit.baseSpeed}")
#         print(f"Vitality:\t{unit.baseVitality}")
#         print(f"Constitution:\t{unit.baseConstitution}")
#         print(f"Intelligence:\t{unit.baseIntelligence}")
#         print(f"Mind:\t\t{unit.baseMind}")
#         print(f"Resistance:\t{unit.baseResistance}")
#         print(f"You would deal {get_melee_damage(unit)} melee damage.")
#         print(f"You have a {unit.melee_hit_chance}% chance to hit.")
#         print(f"You have {unit.basePhysicalResistance}% Physical Resistance.")
#         if unit.weaponslot1:
#             print(f"You have a {unit.weaponslot1.name} equipped.")