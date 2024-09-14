import Unit
import Stats

handed = ("onehanded", "twohanded")
damagetype = ("Slashing", "Piercing", "Crushing")





class Inventory:

      war_funds = 1000

      def __init__(self, capacity):
            self.capacity = capacity
            self.items = []



      def discard(item, inventory):
                  inventory.items.remove(item)

      def display_inv(inventory):
            if not inventory.items:
                  print("\nYou have no items in your inventory.\n")
            else:
                  print("Inventory: ----------------------")
                  for items in inventory.items:
                        print(f"| ID:{items.itemid} {items.name}", end = " ")
      


class Item:
      
      slot_types = ("weaponslot1", "weaponslot2", "weaponslot3", "helmetslot", "armorslot", "legslot", "ringslot")
      lastknownitemid = 0

      def __init__(self, name, weight, value):
            self.name = name
            self.weight = weight
            self.value = value
            self.slot_type = ""



            Item.lastknownitemid += 1
            self.itemid = Item.lastknownitemid

      #def equip(item, unit, slot):
      #      pass

      #def unequip(item, unit, slot):
      #      pass



      def equip(self, unit, slot_type, inventory):

            unit_equipment = unit.get_equipment_as_dict()
            #print(self)
            

            for key, value in unit_equipment.items():
                  if key == slot_type:
                        if value == None:
                              setattr(unit, slot_type, self)
                              
                        else:
                              print("slot already taken")
            

            self.slot_type = slot_type
            #print(self.slot_type)
            #print(slot_type)
            inventory.items.remove(self)


      def unequip(self, unit, slot_type, inventory):

            slot_type = self.slot_type

            unit_equipment = unit.get_equipment_as_dict()

            for key, value in unit_equipment.items():
                  if key == slot_type:
                        if value:
                              inventory.items.append(value)
                              setattr(unit, key, None)
                              #print(value)


            # for key, item in unit_equipment.items():
            #       if item:
            #             if item.name == self.name:
            #                   inventory.items.append(item)
            #                   unit_equip_slot = setattr(unit, key, None)
            #                   print(unit_equip_slot)


      def get_item_by_id(id, inventory = None, unit = None):
            if inventory:
                  for item in inventory.items:
                        if id == item.itemid:
                              return item
            elif unit:
                  for unit in Unit.unitlist:
                        if id == unit.weaponslot1.itemid:
                              return unit.weaponslot1

                  
      def display_stats(item, option = 0):
            display_stats = [f'Item ID: {item.itemid}',
                    f'Name:\t{item.name}',
                    f'Value:\t\t{item.value}',
                    ]
            
            if option == 1:
                  pass

            return '\n'.join(display_stats)




class Weapon(Item):

      def __init__(self, name, weight, value, handed, damagetype, damagerange):
            super().__init__(name, weight, value)
            self.handed = handed
            self.damagetype = damagetype
            self.damagerange = damagerange
            self.slot_type = ""
  


            

class Armor(Item):

      def __init__(self, name, weight, value, armortype, slashingreduction = 0, piercingreduction = 0, crushingreduction = 0):
            super().__init__(name, weight, value)
            self.armortype = armortype
            self.slashingreduction = slashingreduction
            self.piercingreduction = piercingreduction
            self.crushingreduction = crushingreduction
            self.slot_type = ""



# weapons_dict = {
#       'Iron Short Sword': Weapon("Iron Short Sword", 4, 50, "one-handed", "Slashing", 6),


# }