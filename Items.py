

handed = ("onehanded", "twohanded")
damagetype = ("Slashing", "Piercing", "Crushing")




class Inventory:
      def __init__(self, capacity):
            self.capacity = capacity
            self.items = []


class Weapon:

    lastknownitemid = 0

    def __init__(self, name, handed, weight, damagetype, damagerange, value):
            self.name = name
            self.handed = handed
            self.weight = weight
            self.damagetype = damagetype
            self.damagerange = damagerange
            self.value = value

            Weapon.lastknownitemid += 1
            self.itemid = Weapon.lastknownitemid



def equip(weapon, unit):
      
      unit.weaponslot1 = weapon
      





#class Armor:


#class Shield:

#weapon = Weapon("Iron Short Sword", handed, 4, "Slashing", (6, 8))

#print(weapon.name)





weapons_dict = {
      'Iron Short Sword': Weapon("Iron Short Sword", "one-handed", 4, "Slashing", 6, 50),
      'Iron Greatsword': Weapon("Iron Greatsword", "two-handed", 8, "Slashing", 12, 100),
      'Iron Rapier': Weapon("Iron Rapier", "one-handed", 3, "Piercing", 6, 75),


}