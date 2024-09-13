

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
      
      lastknownitemid = 0

      def __init__(self, name, weight, value):
            self.name = name
            self.weight = weight
            self.value = value

            Item.lastknownitemid += 1
            self.itemid = Item.lastknownitemid

      def equip(item, unit, slot):
            pass

      def unequip(item, unit, slot):
            pass


      def get_item_by_id(id, inventory):
            for item in inventory.items:
                  if id == item.itemid:
                        return item
                  
      def display_stats(item, option = 0):
            display_stats = [f'ID: {item.itemid}',
                    f'Name: {item.name}',
                    f'Damage:\t{item.damagerange}',
                    f'Value:\t{item.value}',
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

      def equip(weapon, unit, slot, inventory):
            if slot == 1:
                  unit.weaponslot1 = weapon
            if slot == 2:
                  unit.weaponslot2 = weapon

            inventory.items.remove(weapon)

      def unequip(unit, slot, inventory):
            if slot == 1:
                  slot = unit.weaponslot1

                  inventory.items.append(slot)
                  unit.weaponslot1 = None

            elif slot == 2:
                  slot = unit.weaponslot2

                  inventory.items.append(slot)
                  unit.weaponslot2 = None
            
            
            


            

class Armor(Item):

      def __init__(self, name, weight, value, armortype, slashingreduction, piercingreduction, crushingreduction):
            super().__init__(name, weight, value)
            self.armortype = armortype
            self.slashingreduction = slashingreduction
            self.piercingreduction = piercingreduction
            self.crushingreduction = crushingreduction



weapons_dict = {
      'Iron Short Sword': Weapon("Iron Short Sword", 4, 50, "one-handed", "Slashing", 6),


}