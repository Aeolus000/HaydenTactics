import random
from sqlalchemy import String, select, ForeignKey, delete
from sqlalchemy.orm import Session, mapped_column
from sqlalchemy import create_engine, update


import Unit
import Items
import Stats
from Models import *


class UnitService:
    @classmethod
    def generate_unit_stats(self):

        base_str = 10 + random.randrange(-2, 3)
        base_dex = 10 + random.randrange(-2, 3)
        base_spd = 10 + random.randrange(-2, 3)
        base_vit = 10 + random.randrange(-2, 3)
        base_con = 10 + random.randrange(-2, 3)
        base_int = 10 + random.randrange(-2, 3)
        base_mnd = 10 + random.randrange(-2, 3)
        base_res = 10 + random.randrange(-2, 3)

        return {
            'exp': 0,
            'is_alive': True,
            'action_points': 0,
            'base_str': base_str,
            'base_dex': base_dex,
            'base_spd': base_spd,
            'base_vit': base_vit,
            'base_con': base_con,
            'base_int': base_int,
            'base_mnd': base_mnd,
            'base_res': base_res,
            'max_hp': 75 + (4 * base_vit),
            'current_hp': 75 + (4 * base_vit),
            'max_mana': 10 + (2 * base_mnd),
            'current_mana': 0,
            'melee_hit_chance': 70 + (base_dex // 5),
            'ranged_hit_chance': 50 + (base_dex // 4),
            'base_phys_res': (base_con * 0.5),
            'base_mag_res': (base_res * 0.5),
            'base_phys_evasion': 0,
            'base_mag_evasion': 0,
            'initiative': 0,
            'weapon_slot1': None,
            'weapon_slot2': None,
            'weapon_slot3': None,
            'helmet_slot': None,
            'armor_slot': None,
            'leg_slot': None,
            'ring_slot': None,
                } 

    @classmethod
    def create(self, name, charclass, level = 1, stats = None, team = 0):
        
        if not stats:
            stats = self.generate_unit_stats()

        #print(stats)

        with Session(engine) as session:

            table_unit = UnitTable(
                name=name,
                charclass=charclass,
                level=level,
                team=team,
                exp=0,
                is_alive=True,
                base_str=stats['base_str'],
                base_dex=stats['base_dex'],
                base_spd=stats['base_spd'],
                base_vit=stats['base_vit'],
                base_con=stats['base_con'],
                base_int=stats['base_int'],
                base_mnd=stats['base_mnd'],
                base_res=stats['base_res'],
                max_hp=stats['max_hp'],
                current_hp=stats['current_hp'],
                max_mana=stats['max_mana'],
                current_mana=stats['current_mana'],
                melee_hit_chance=stats['melee_hit_chance'],
                ranged_hit_chance=stats['ranged_hit_chance'],
                base_phys_res=stats['base_phys_res'],
                base_mag_res=stats['base_mag_res'],
                base_phys_evasion=stats['base_phys_evasion'],
                base_mag_evasion=stats['base_mag_evasion'],
            )
            session.add(table_unit)
            session.commit()

            table_unit_inv = UnitEquipmentTable(
                unit_id=table_unit.id,
                weapon_slot1=1,
                weapon_slot2=None,
                weapon_slot3=None,
                helmet_slot=None,
                armor_slot=None,
                leg_slot=None,
                ring_slot=None,
            )
            session.add(table_unit_inv)
            session.commit()


    @classmethod
    def generate_random_unit(self, team = 0):

        if len(Unit.nameslist) <= 0:
            #randomname = "Out Of Names"
            Unit.nameslist.extend(["Aeolus", "Abraxis", "Zeyta", "Zalzaide", "Armagus", "Ibane", "Gen'jin", "Byron", "Jaeremy", "Artemisia", "Judica", 
                "Adalinde", "Olivia", "Garth", "Erebus", "Marius", "Daniel", "Selene", "Liam", "Hayden", "Jessica", "Kayloc", 
                "Tetsedah", "Soultrax", "Tsoul", "Anathros", "Sathson", "Brody", "Cameron", "Brock", "Kevin", "Alessandro", 
                "Madeline", "Thomas", "Delwin Praeg", "Ryan", "Justin", "McCray", "Chase", "Elyse", "Noah", "Stephen", "Carlton", "Honeyglow", "Austyn"])

        randomname = random.choice(Unit.nameslist)
        Unit.nameslist.remove(randomname)

        charclass = random.choice(Unit.charclasses)


        randomized_unit = UnitService.create(randomname, charclass, 1, team = team)
        #randomunit = Unit(randomname, charclass, 1)
        return randomized_unit
    
    @classmethod
    def generate_enemy_team(self):
        self.generate_random_unit(team = 1)
        self.generate_random_unit(team = 1)
        self.generate_random_unit(team = 1)

    @classmethod
    def get_nonplayer_units(self):
        with Session(engine) as session:

            units = session.query(UnitTable).filter(UnitTable.team > 0)

            session.flush()

        return units
    
    @classmethod
    def delete_nonplayer_units(self):

        with Session(engine) as session:

            #session.query(UnitTable).filter(UnitTable.team >= 1).delete
            stmt = delete(UnitTable).where(UnitTable.team >= 1)
            session.execute(stmt)
            #session.delete(UnitTable).where(UnitTable.team >= 1)
            #units = select(UnitTable).where(UnitTable.team >= 1)
            #session.delete(units)

            session.commit()
            session.flush()

    @classmethod
    def get_all(self):
        with Session(engine) as session:

            units = session.query(UnitTable).all()

        return units
    
    @classmethod
    def get_all_as_dict(self):

        unitlist = []
        with Session(engine) as session:
            test = session.query(UnitTable).all()

            for item in test:

                equipdict, weapondict = self.get_unit_equipment(item.id)

                unitdict = {'id': item.id,
                        'name': item.name,
                        'charclass': item.charclass,
                        'level': item.level,
                        'team': item.team,
                        'exp': item.exp,
                        'is_alive': item.is_alive,
                        'action_points': 0,
                        'move_points': 0,
                        'death_timer': 0,
                        'permadeath': False,
                        'wait': False,
                        'max_hp': item.max_hp,
                        'current_hp': item.current_hp,
                        'max_mana': item.max_mana,
                        'current_mana': item.current_mana,
                        'melee_hit_chance': item.melee_hit_chance,
                        'ranged_hit_chance': item.ranged_hit_chance,
                        'base_phys_res': item.base_phys_res,
                        'base_mag_res': item.base_mag_res,
                        'base_phys_evasion': 0,
                        'base_mag_evasion': 0,
                        'initiative': 0,
                        'base_str': item.base_str,
                        'base_dex': item.base_dex,
                        'base_spd': item.base_spd,
                        'base_vit': item.base_vit,
                        'base_con': item.base_con,
                        'base_int': item.base_int,
                        'base_mnd': item.base_mnd,
                        'base_res': item.base_res,

                        'weapon_slot1': weapondict.__dict__,
                        #'weapon_slot2': equipdict
                        }
            
                unitlist.append(unitdict)

        return unitlist

    def get_attributes_by_id(unit_id):

        with Session(engine) as session:

            unit = session.query(UnitTable).get(unit_id)                ### this returns the whole row properly
    
        return unit
    
    def get_unit_by_row(selection):

        with Session(engine) as session:

            unitslol = session.query(UnitTable).all()              ### how do i get a specific row by number???
            unit = unitslol[selection]
    
        return unit
    
    def get_unit_equipment(unit_id):

        with Session(engine) as session:

            #unit = session.query(UnitTable).get(unit_id)

            equipment = session.query(UnitEquipmentTable).get(unit_id)

            weapon = session.query(BaseWeaponTable).get(equipment.weapon_slot1)

        return equipment, weapon
    
    def refresh_stats_noncombat(unit):

        with Session(engine) as session:

            session.query(UnitTable).filter(UnitTable.id == unit.id).update({'max_hp': 75 + (4 * unit.base_vit)})
            session.query(UnitTable).filter(UnitTable.id == unit.id).update({'current_hp': 75 + (4 * unit.base_vit)})
            session.query(UnitTable).filter(UnitTable.id == unit.id).update({'max_mana': 10 + (2 * unit.base_mnd)})
            session.query(UnitTable).filter(UnitTable.id == unit.id).update({'current_mana': 0})
            session.query(UnitTable).filter(UnitTable.id == unit.id).update({'melee_hit_chance': 70 + (unit.base_dex // 5)})
            session.query(UnitTable).filter(UnitTable.id == unit.id).update({'ranged_hit_chance': 50 + (unit.base_dex // 4)})
            session.query(UnitTable).filter(UnitTable.id == unit.id).update({'base_phys_res': (unit.base_con * 0.5)})
            session.query(UnitTable).filter(UnitTable.id == unit.id).update({'base_mag_res': (unit.base_res * 0.5),})

            session.commit()
            session.flush()
    
    def level_up(unit):
        
        stats = Stats.levelup_stats[unit.charclass]

        with Session(engine) as session:
            unit.level = unit.level + 1

            session.query(UnitTable).filter(UnitTable.id == unit.id).update({'level': unit.level})

            for key, value in stats.as_dict().items():

                unit_current_stat = getattr(unit, key)

                session.query(UnitTable).filter(UnitTable.id == unit.id).update({key: unit_current_stat + value})


            session.commit()
            session.flush()         

    def dismiss(unit):

        with Session(engine) as session:
            session.delete(unit)

            session.commit()
            session.flush()

class WeaponService:
    def populate_weapons():

        ### need to check if this is empty before I create it, otherwise it creates it over nad over
        with Session(engine) as session:

            weapons = [
                {
                    'name': 'Iron Short Sword',
                    'weight': 4, 
                    'value': 50, 
                    'handed': "one-handed", 
                    'damage_type': "Slashing", 
                    'damage_range': 8
                },
                {
                    'name': 'Iron Greatsword',
                    'weight': 8, 
                    'value': 80, 
                    'handed': "two-handed", 
                    'damage_type': "Slashing", 
                    'damage_range': 14
                },
                {
                    'name': 'Iron Rapier',
                    'weight': 3, 
                    'value': 60, 
                    'handed': "one-handed", 
                    'damage_type': "Piercing", 
                    'damage_range': 7
                },
                {
                    'name': 'Iron Morning Star',
                    'weight': 5, 
                    'value': 60, 
                    'handed': "one-handed", 
                    'damage_type': "Crushing", 
                    'damage_range': 6
                },
                {
                    'name': 'Iron Handaxe',
                    'weight': 3, 
                    'value': 40, 
                    'handed': "one-handed", 
                    'damage_type': "Slashing", 
                    'damage_range': 6
                },
                {
                    'name': 'Iron Spear',
                    'weight': 5, 
                    'value': 75, 
                    'handed': "one-handed", 
                    'damage_type': "Piercing", 
                    'damage_range': 6
                },
                {
                    'name': 'Iron Halberd',
                    'weight': 9, 
                    'value': 100, 
                    'handed': "two-handed", 
                    'damage_type': "Slashing", 
                    'damage_range': 8
                },
                {
                    'name': 'Wooden Staff',
                    'weight': 4, 
                    'value': 25, 
                    'handed': "one-handed", 
                    'damage_type': "Crushing", 
                    'damage_range': 4
                },
            ]

            for weapon in weapons:
                db_weapon = BaseWeaponTable(
                    name=weapon['name'],
                    weight=weapon['weight'],
                    value=weapon['value'],
                    handed=weapon['handed'],
                    damage_type=weapon['damage_type'],
                    damage_range=weapon['damage_range'],
                )

                session.add(db_weapon)
            session.commit()



engine = create_engine("sqlite:///database.db", echo=False)

Base.metadata.create_all(engine)