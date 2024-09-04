import Unit 
import Stats
import Items



def main():
    is_running = True

    inventory = None

    while is_running:
        print(f"\n\n(1)\tRoster Menu.")
        print(f"(2)\tView Roster (Quick Summary).")
        print(f"(3)\tManage Inventory.")
        print(f"(4)\tBattlefield.")

        print(f"(5)\tExit.")
        option = input("Enter an option: ")

        if option == "1":
            in_roster = True
            while in_roster == True:
                print("\nQuick Reference:")
                print("****************")
                for unit in Unit.unitlist:
                    print(unit.id, unit.name, end = "  ")
                
                print(f"\n\n(1)\tView Character (by ID)")
                print(f"(2)\tCreate Character")
                print(f"(3)\tCreate Random Character")
                print(f"(4)\tLevel up a Character")
                print(f"(5)\tDismiss a Unit")
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

                if menuchoice == "3":          
                    unit = Unit.generate_random_unit()
                    print(f"Created random unit: {unit.name} with ID {unit.lastknownid}\n")

                if menuchoice == "4":
                    for unit in Unit.unitlist:
                        print(f"{unit.id} {unit.name}", end = " ")
                    
                    levelunit_id = int(input("\nChoose the ID of the unit to level up: \n"))

                    levelunit = Unit.get_unit_by_id(levelunit_id)        
                    Unit.level_up(levelunit)

                if menuchoice == "5":
                    for unit in Unit.unitlist:
                            print(unit.id, unit.name, end = "  ")

                    unitid = (int(input("\nChoose a Character to dismiss (ID): ")))

                    unit = Unit.get_unit_by_id(unitid)

                    confirm = (input("Are you sure? Y/N ")).lower()

                    if confirm == "y":
                        Unit.unitlist.remove(unit)
                    elif confirm == "n":
                        pass
                    else:
                        pass
                              


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

        if option == "3":
            in_inventory = True
            if not inventory:
                inventory = Items.Inventory(50)

            while in_inventory:
                
                Items.Inventory.display_inv(inventory)
                    

                print("\n(1) Equip Item to Character.")
                print("(2) Unequip Item from Character.")
                print("(3) Discard Item from Inventory.")
                print("(4) Purchase an Item.")
                print("(5) Back to Main Menu.\n")

                inv_menu_input = input("Choose an option: ")

                if inv_menu_input == "1":
                    
                    Items.Inventory.display_inv(inventory)

                    if not Unit.unitlist:
                        print("")
                        print("!!! --- You don't have any Units --- !!!")
                        print("")
                    else:   
                        item_id = int(input("Choose an Item to equip (ID): "))

                        item = Items.Item.get_item_by_id(item_id, inventory)

                        for unit in Unit.unitlist:
                            print(f"{unit.id}) {unit.name}")

                        equiper_id = int(input(f"Choose a character ID to equip {item.name} onto: "))

                        equiper = Unit.get_unit_by_id(equiper_id)

                        hand = input("(L)eft or (R)ight hand? ").lower()

                        ###testing for % damage reduction actually working or not, this sword normally wouldn't have 1000 damage
                        #weapon = Items.Weapon("Iron Short Sword", 4, 50, "one-handed", "Slashing", 1000)

                        if hand == "r":
                            Items.Weapon.equip(item, equiper, 1, inventory)
                        elif hand == "l":
                            Items.Weapon.equip(item, equiper, 2, inventory)
                        else:
                            print("Invalid option.")

                        



                if inv_menu_input == "2":

                    for unit in Unit.unitlist:
                        if unit.weaponslot1 or unit.weaponslot2 or unit.weaponslot3:
                            Unit.display_unit(unit, 1)

                    unit_id = (int(input("Choose a Unit to unequip (ID): ")))
                               
                    unit = Unit.get_unit_by_id(unit_id)

                    Items.Weapon.unequip(unit, 1 and 2, inventory)
                    

                if inv_menu_input == "3":
                    Items.Inventory.display_inv(inventory)

                    if not inventory.items:
                        pass
                    else:

                        itemid = int(input("Choose an Item to discard (ID): "))

                        discard = Items.Item.get_item_by_id(itemid, inventory)

                        Items.Inventory.discard(discard, inventory)

                if inv_menu_input == "4":

                    print(f"War Funds: {Items.Inventory.war_funds}")

                    print("added Iron Short Sword to inventory. - 100 War Funds")

                    inventory.items.append(Items.Weapon("Iron Short Sword", 4, 50, "one-handed", "Slashing", 6))




                if inv_menu_input == "5":
                    in_inventory = False






                #sword = Items.Weapon("Iron Greatsword", 1, 1, None, None, None)
                #inventory.items.append(sword)
                #Items.Inventory.discard(sword, inventory)


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