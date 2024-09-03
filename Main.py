import Unit 
import Stats
import Items



def main():
    is_running = True

    while is_running:
        print(f"(1)\tRoster Menu.")
        print(f"(2)\tView Roster (Quick Summary).")
        print(f"(3)\tView Inventory.")
        print(f"(4)\tBattlefield.")

        print(f"(5)\tExit.")
        option = input("Enter an option: ")

        if option == "1":
            in_roster = True
            while in_roster == True:
                print("Quick Reference:")
                print("****************")
                for unit in Unit.unitlist:
                    print(unit.id, unit.name, end = "  ")
                
                print(f"\n\n(1)\tView Character (by ID)")
                print(f"(2)\tEquip Character (by ID)")
                print(f"(3)\tCreate Character")
                print(f"(4)\tCreate Random Character")
                print(f"(5)\tLevel up a Character")
                print(f"(6)\tBack to Main Menu")

                menuchoice = input("Choose option #: ")

                if menuchoice == "1":
                    if not Unit.unitlist:
                        print("")
                        print("!!! --- You don't have any Units --- !!!")
                        print("")
                    else:

                        for unit in Unit.unitlist: 
                            print(unit.id, unit.name, end = "  ")

                        unitchoice_id = int(input("\nChoose a Unit ID: "))
                        unitchoice = Unit.get_unit_by_id(unitchoice_id)

                        Unit.display_unit(unitchoice, 2)

                if menuchoice == "2":
                    if not Unit.unitlist:
                        print("")
                        print("!!! --- You don't have any Units --- !!!")
                        print("")
                    else:

                        inventory = Items.Inventory(50)
                        for unit in Unit.unitlist:
                            print(f"{unit.id}) {unit.name}")

                        equiper_id = int(input("Choose a character ID to equip an Iron Short Sword onto: "))

                        equiper = Unit.get_unit_by_id(equiper_id)

                        hand = input("(L)eft or (R)ight hand? ").lower()

                        #testing for % damage reduction actually working or not, this sword normally wouldn't have 1000 damage
                        weapon = Items.Weapon("Iron Short Sword", 4, 50, "one-handed", "Slashing", 1000)

                        if hand == "r":
                            Items.Weapon.equip(weapon, equiper, 1)
                        if hand == "l":
                            Items.Weapon.equip(weapon, equiper, 2)
                        else:
                            print("Invalid option.")

             
                if menuchoice == "3": 
                    
                    namechoice = input("Name the character: ")

                    i = 1
                    for charclass in Unit.charclasses: 
                        print(f"{i}: {charclass}")
                        i += 1

                    charclasschoice = int(input("Choose their class ID: "))
                    for i, classname in enumerate(Unit.charclasses):
                        if charclasschoice == i + 1:
                            charclasschoice = classname

                    unit = Unit.Unit(namechoice, charclasschoice, 1)
                    Unit.unitlist.append(unit)

                if menuchoice == "4":          
                    unit = Unit.generate_random_unit()
                    print(f"Created random unit: {unit.name} with ID {unit.lastknownid}\n")

                if menuchoice == "5":
                    for unit in Unit.unitlist:
                        print(f"{unit.id}) {unit.name}")
                    
                    levelunit_id = int(input("Choose the ID of the unit to level up: \n"))

                    levelunit = Unit.get_unit_by_id(levelunit_id)        
                    Unit.level_up(levelunit)

                if menuchoice == "6":
                    in_roster = False

        if option == "2":
            if not Unit.unitlist:
                print("")
                print("!!! --- You don't have any Units --- !!!")
                print("")
            else:
                for unit in Unit.unitlist:
                    Unit.display_unit(unit, 1)
                print("\n************************\n")

        if option == "4":
            for unit in Unit.unitlist:
                print(f"{unit.id}) {unit.name}")
            unit_id1 = int(input("Choose an attacker ID from the above units: "))
            unit_id2 = int(input("Choose the opponent unit ID: "))
            
            unit1 = Unit.get_unit_by_id(unit_id1)
            unit2 = Unit.get_unit_by_id(unit_id2)
            Unit.attack(unit1, unit2)



        if option == "5":
            is_running = False
        



if __name__ == "__main__":
    main()