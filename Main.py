import Unit 
import Stats
import Items



def main():
    is_running = True

    while is_running:
        print(f"(1)\tView Roster.")
        print(f"(2)\tList all current units and their stats.")
        print(f"(3)\tList all current units.")
        print(f"(4)\tHave a unit attack another.")
        print(f"(5)\tLevel up a unit.")
        print(f"(6)\tEquip a weapon on a unit.")
        print(f"(7)\tExit.")
        option = input("Enter an option: ")

        if option == "1":
            in_roster = True
            while in_roster == True:
                for unit in Unit.unitlist:
                    print(unit.id, unit.name, end = "  ")

                print(f"\n(1)\tView Character (by ID)")
                print(f"(2)\tEquip Character (by ID)")
                print(f"(3)\tCreate Character")
                print(f"(4)\tCreate Random Character")

                menuchoice = input("Choose option #: ")

                if menuchoice == "1":

                    for unit in Unit.unitlist: 
                        print(unit.id, unit.name, end = "  ")

                    unitchoice = int(input("\nChoose a Unit ID: "))
                    for unit in Unit.unitlist:
                        if unitchoice == unit.id:
                            unitchoice = unit

                            Unit.display_unit(unit, 1)

                            


                if menuchoice == "4":          
                    unit = Unit.generate_random_unit()
                    print(f"Created random unit: {unit.name} with ID {unit.lastknownid}")


            



        if option == "3":
            for unit in Unit.unitlist:
                Unit.display_unit(unit)


        if option == "4":
            for unit in Unit.unitlist:
                print(f"{unit.id}) {unit.name}")
            unit1 = int(input("Choose an attacker ID from the above units: "))
            unit2 = int(input("Choose the opponent unit ID: "))
            
            for unit in Unit.unitlist:
                if unit1 == unit.id:
                    unit1 = unit

            for unit in Unit.unitlist:
                if unit2 == unit.id:
                    unit2 = unit
            

            Unit.attack(unit1, unit2)

        if option == "5":
            for unit in Unit.unitlist:
                print(f"{unit.id}) {unit.name}")
            
            levelunit = int(input("Choose the ID of the unit to level up: "))

            for unit in Unit.unitlist:
                if levelunit == unit.id: 
                    levelunit = unit
                    
            Unit.level_up(levelunit)

        if option == "6": 
            inventory = Items.Inventory(1)
            for unit in Unit.unitlist:
                print(f"{unit.id}) {unit.name}")

            Equiper = int(input("Choose a character ID to equip an Iron Short Sword onto: "))

            for unit in Unit.unitlist:
                if Equiper == unit.id: 
                    Equiper = unit

            #inventory.items.append(Items.Weapon("Iron Short Sword", "handed", 4, "Slashing", 6, 50))
            #print(inventory.items)
            #print("Added weapon")
            weapon = Items.Weapon("Iron Short Sword", "handed", 4, "Slashing", 6, 50)
            Items.equip(weapon, unit)


            #Items.Weapon.equip((Items.Weapon("Iron Short Sword", "handed", 4, "Slashing", 8, 50)), Equiper)
            


        if option == "7":  
            is_running = False





if __name__ == "__main__":
    main()