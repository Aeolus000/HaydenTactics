import Unit
import Items
import Stats



turn_count = 1

tick_running = True

unit1 = Unit.Unit("Hayden", "weaponmaster", 1)
unit2 = Unit.Unit("Jessica", "weaponmaster", 1)
#unit3 = Unit.Unit("bro3", "weaponmaster", 1)

Unit.unit_list.append(unit1)
Unit.unit_list.append(unit2)
#Unit.unit_list.append(unit3)


while tick_running:

    for unit in Unit.unit_list:
        speed = unit.base_speed
        current_initiative = unit.initiative

        unit.initiative = current_initiative + speed

        print(unit.name, speed, current_initiative)

        #print(unit.name, unit.initiative)
        
        if unit.initiative >= 100:
            #print(unit.name, unit.initiative)

            rollover_initiative = unit.initiative - 100

            current_turn_unit = unit
            
            print(current_turn_unit.name)



            tick_running = False

            turn_action = input("take your turn, (press 1 NOW): ")
            #take_turn()
            if turn_action == "1":
                    unit.initiative = 0 + rollover_initiative

                    turn_count = turn_count + 1
                    print(turn_count)
                    tick_running = True





    

def take_turn():

    turn_finished = False
    move_range = 0
    wait = 0

    ## while loop?
    ##      move            can't use this yet, but if you click it it should grey out since you should only get one move action per turn
    ##      attack          -1 AP           if 0 AP: grey out
    ##      ability         -x AP           if 0 AP: grey out
    ##      wait            depending on how much AP you have left, you are refunded some initiative. Otherwise set to 0

    if wait == 2:
         current_turn_unit.initiative = 50
    elif wait == 1:
         current_turn_unit.initiative = 25
    else:
         current_turn_unit.initiative = 0


    turn_finished = True




def choose_target():
     

    ##          target = currentrow of enemy list
    ##          current row is index of enemy_unit_list
    ##          run attack function to see if it hit
    ##          reduce current_hp of enemy unit if hit
    ##          remove 1AP from the unit for the attack command

    pass 