

handed = ("onehanded", "twohanded")
damagetype = ("Slashing", "Piercing", "Crushing")





class Inventory:
      def __init__(self, capacity):
            self.capacity = capacity
            self.items = []


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

      def remove(item, unit, slot):
            pass

class Weapon(Item):

      def __init__(self, name, weight, value, handed, damagetype, damagerange):
            super().__init__(name, weight, value)
            self.handed = handed
            self.damagetype = damagetype
            self.damagerange = damagerange

      def equip(weapon, unit, slot):
            if slot == 1:
                  unit.weaponslot1 = weapon
            if slot == 2:
                  unit.weaponslot2 = weapon

class Armor(Item):

      def __init__(self, name, weight, value, armortype, slashingreduction, piercingreduction, crushingreduction):
            super().__init__(name, weight, value)
            self.armortype = armortype
            self.slashingreduction = slashingreduction
            self.piercingreduction = piercingreduction
            self.crushingreduction = crushingreduction



weapons_dict = {
      'Iron Short Sword': Weapon("Iron Short Sword", 4, 50, "one-handed", "Slashing", (6, 8)),


}