import random
from sqlalchemy import String, select, ForeignKey
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


import Unit
import Items
import Stats
from Models import UnitTable, Base


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
            'current_mana':10 + (2 * base_mnd),
            'melee_hit_chance': 70 + (base_dex / 5),
            'ranged_hit_chance': 50 + (base_dex / 4),
            'base_phys_res': (base_con * 0.5),
            'base_mag_res': (base_res * 0.5),
            'base_evasion': 0,
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
    def create(self, name, charclass, level = 1, stats = None):
        
        if not stats:
            stats = self.generate_unit_stats()

        #print(stats)

        with Session(engine) as session:

            table_unit = UnitTable(
                name=name,
                charclass=charclass,
                level=level,
                exp=0,
                is_alive=True,
                action_points=0,
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
                base_evasion=stats['base_evasion'],
                initiative=stats['initiative'],

            )
            session.add(table_unit)
            session.commit()

            #print(table_unit.id)

            #stmt = select('*').select_from(Models.UnitTable)
            #result = session.execute(stmt).fetchall
            #print(result.one())
            #print(result)

    @classmethod
    def generate_random_unit(self):

        if len(Unit.nameslist) <= 0:
            #randomname = "Out Of Names"
            Unit.nameslist.extend(["Aeolus", "Abraxis", "Zeyta", "Zalzaide", "Armagus", "Ibane", "Gen'jin", "Byron", "Jaeremy", "Artemisia", "Judica", 
                "Adalinde", "Olivia", "Garth", "Erebus", "Marius", "Daniel", "Selene", "Liam", "Hayden", "Jessica", "Kayloc", 
                "Tetsedah", "Soultrax", "Tsoul", "Anathros", "Sathson", "Brody", "Cameron", "Brock", "Kevin", "Alessandro", 
                "Madeline", "Thomas", "Delwin Praeg", "Ryan", "Justin", "McCray", "Chase", "Elyse", "Noah", "Stephen", "Carlton", "Honeyglow", "Austyn"])

        randomname = random.choice(Unit.nameslist)
        Unit.nameslist.remove(randomname)

        charclass = random.choice(Unit.charclasses)


        randomized_unit = UnitService.create(randomname, charclass, 1)
        #randomunit = Unit(randomname, charclass, 1)
        return randomized_unit

    @classmethod
    def get_all(self):
        with Session(engine) as session:
            

            #row = session.execute(select(UnitTable.name, UnitTable.id)).all()
            #blah = select(UnitTable).where(UnitTable.id >= 1)
            #row = session.execute(blah)

            #blah2 = session.execute(select(UnitTable.all()).where(UnitTable.id >= 1))

            test = session.query(UnitTable).all()
            # for item in test:
            #     print(item.name)
            #     print(item.id)

            #print(db_return)

        return test

    def get_attributes_by_id(unit_id):

        with Session(engine) as session:

            #test = session.query(UnitTable).where(UnitTable.id == unit_id)
            unit = session.query(UnitTable).get(unit_id)                ### this returns the whole row properly

            #esult = session.execute(test)

        
    
        return unit




engine = create_engine("sqlite:///database.db", echo=True)

Base.metadata.create_all(engine)




