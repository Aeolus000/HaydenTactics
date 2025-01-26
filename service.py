import random
from sqlalchemy import String, select, ForeignKey, delete
from sqlalchemy.orm import Session, mapped_column
from sqlalchemy import create_engine, update


import Unit
import Items
import Stats
from Models import *

nameslist = ["Aeolus", "Abraxis", "Zeyta", "Zalzaide", "Armagus", "Ibane", "Gen'jin", "Byron", "Jaeremy", "Artemisia", "Judica", 
                "Adalinde", "Olivia", "Garth", "Erebus", "Marius", "Daniel", "Selene", "Liam", "Hayden", "Jessica", "Kayloc", 
                "Tetsedah", "Soultrax", "Tsoul", "Anathros", "Sathson", "Brody", "Cameron", "Brock", "Kevin", "Alessandro", 
                "Madeline", "Thomas", "Delwin Praeg", "Ryan", "Justin", "McCray", "Chase", "Elyse", "Noah", "Stephen", "Carlton", "Honeyglow", "Austyn", "Abelard",
                "Addison",
                "Alaire",
                "Aleyn",
                "Ancel",
                "Ande",
                "Anselm",
                "Arnald",
                "Arnott",
                "Arthur",
                "Augustine",
                "Aylmer",
                "Baldric",
                "Bartholomew",
                "Belmont",
                "Benedict",
                "Bernard",
                "Berndan",
                "Bertram",
                "Bertrand",
                "Bouchard",
                "Boyle",
                "Brice",
                "Brien",
                "Bryce",
                "Cain",
                "Caplan",
                "Claudien",
                "Clifton",
                "Clive",
                "Cuthbert",
                "Daimbert",
                "Dawson",
                "Derwin",
                "Deryk",
                "Drew",
                "Drystan",
                "Eadbert",
                "Ealdwine",
                "Eddard",
                "Edwyn",
                "Eldred",
                "Emanuel",
                "Esmond",
                "Esmour",
                "Fiebras",
                "Flambard",
                "Foxe",
                "Francis",
                "Frederyk",
                "Fulke",
                "Ganelon",
                "Geoffrey",
                "Gerald",
                "Gerbold",
                "Goddard",
                "Godebert",
                "Gylbart",
                "Gyles",
                "Halstein",
                "Hamon",
                "Heinlein",
                "Hewrey",
                "Higelin",
                "Ivan",
                "Jakys",
                "Jeger",
                "Jeorge",
                "Jonathas",
                "Joseph",
                "Josias",
                "Kain",
                "Kenrick",
                "Ladislas",
                "Laurence",
                "Laurentius",
                "Leavold",
                "Lodwicke",
                "Mansel",
                "Marlowe",
                "Mathye",
                "Morys",
                "Myles",
                "Navarre",
                "Noah",
                "Olyver",
                "Orrick",
                "Oswyn",
                "Parnell",
                "Peter",
                "Powle",
                "Radolf",
                "Randwulf",
                "Reeve",
                "Reinholdt",
                "Reynard",
                "Ribald",
                "Richarde",
                "Ridel",
                "Roger",
                "Samson",
                "Sandre",
                "Sevrin",
                "Symon",
                "Taran",
                "Taylor",
                "Templeton",
                "Tuckard",
                "Tywick",
                "Valentyne",
                "Viktor",
                "Voyce",
                "Vyncent",
                "Wadard",
                "Warin",
                "Werner",
                "Willielmus",
                "Woden",
                "Wolfstan",
                "Xacheus",
                "Ywain",
                "Adela",
                "Admiranda",
                "Aeditha",
                "Aelina",
                "Agnys",
                "Alainne",
                "Aleria",
                "Alyne",
                "Alys",
                "Alyssa",
                "Amelia",
                "Anna",
                "Annabel",
                "Anne",
                "Arlette",
                "Asha",
                "Atilda",
                "Ava",
                "Avelin",
                "Averille",
                "Ayleth",
                "Beatrix",
                "Bertana",
                "Carmen",
                "Cecillia",
                "Cecily",
                "Celes",
                "Celestine",
                "Celestria",
                "Cenota",
                "Chloe",
                "Christabel",
                "Clarimond",
                "Collys",
                "Concessa",
                "Cwengyth",
                "Damaris",
                "Dametta",
                "Decima",
                "Deloys",
                "Diamanda",
                "Dionisia",
                "Dorcas",
                "Edelinne",
                "Eilonwy",
                "Elle",
                "Elsebee",
                "Eltyana",
                "Elyn",
                "Elynor",
                "Elyzabeth",
                "Emblyn",
                "Emeline",
                "Emeny",
                "Emeria",
                "Emilie",
                "Eschina",
                "Estrild",
                "Ethelia",
                "Evelyn",
                "Faye",
                "Frances",
                "Francisca",
                "Garnet",
                "Germainne",
                "Glenda",
                "Gloriana",
                "Gwenneth",
                "Helena",
                "Helenor",
                "Hester",
                "Hilda",
                "Hildegard",
                "Imedia",
                "Ismenia",
                "Jacquette",
                "Jessica",
                "Jocea",
                "Jocelyn",
                "Joleicia",
                "Jolline",
                "Joyse",
                "Judithe",
                "Julia",
                "Juliana",
                "Kath",
                "Katrina",
                "Konstanze",
                "Lauda",
                "Leofwen",
                "Leofwynn",
                "Lyde",
                "Maerwynn",
                "Malin",
                "Margarete",
                "Margeria",
                "Maronne",
                "Martine",
                "Mathild",
                "Melly",
                "Melusine",
                "Meredithe",
                "Merilda",
                "Meryell",
                "Minerva",
                "Morgayne",
                "Muriel",
                "Nicia",
                "Olyffe",
                "Ophellia",
                "Parnell",
                "Patricya",
                "Pelinne",
                "Penelope",
                "Petronilla",
                "Pulmia",
                "Rebecca",
                "Rosa",
                "Rosamund",
                "Sabrine",
                "Samantha",
                "Sarra",
                "Saya",
                "Scarlet",
                "Somerhild",
                "Sylphie",
                "Sylvia",
                "Syndony",
                "Temperance",
                "Tess",
                "Thomasyn",
                "Thora",
                "Tristana",
                "Vega",
                "Wenda",
                "Wulfhilda",
                "Wynefreede",
                "Yve",]
charclasses = ["Weaponmaster", "Shaman", "Necromancer", "Monk", "Demonologist", "Elementalist", "Rogue", "Hemomancer", "Astromancer", "Crusader", "Priest"]


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
            'max_hp': 50 + (4 * base_vit),
            'current_hp': 50 + (4 * base_vit),
            'max_mana': 10 + (2 * base_mnd),
            'current_mana': 0,
            'melee_hit_chance': 70 + round(base_dex / 5),
            'ranged_hit_chance': 50 + round(base_dex / 4),
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
                weapon_slot1=4,
                weapon_slot2=5,
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

        if len(nameslist) <= 0:
            #randomname = "Out Of Names"
            nameslist.extend(["Aeolus", "Abraxis", "Zeyta", "Zalzaide", "Armagus", "Ibane", "Gen'jin", "Byron", "Jaeremy", "Artemisia", "Judica", 
                "Adalinde", "Olivia", "Garth", "Erebus", "Marius", "Daniel", "Selene", "Liam", "Hayden", "Jessica", "Kayloc", 
                "Tetsedah", "Soultrax", "Tsoul", "Anathros", "Sathson", "Brody", "Cameron", "Brock", "Kevin", "Alessandro", 
                "Madeline", "Thomas", "Delwin Praeg", "Ryan", "Justin", "McCray", "Chase", "Elyse", "Noah", "Stephen", "Carlton", "Honeyglow", "Austyn", "Abelard",
                "Addison",
                "Alaire",
                "Aleyn",
                "Ancel",
                "Ande",
                "Anselm",
                "Arnald",
                "Arnott",
                "Arthur",
                "Augustine",
                "Aylmer",
                "Baldric",
                "Bartholomew",
                "Belmont",
                "Benedict",
                "Bernard",
                "Berndan",
                "Bertram",
                "Bertrand",
                "Bouchard",
                "Boyle",
                "Brice",
                "Brien",
                "Bryce",
                "Cain",
                "Caplan",
                "Claudien",
                "Clifton",
                "Clive",
                "Cuthbert",
                "Daimbert",
                "Dawson",
                "Derwin",
                "Deryk",
                "Drew",
                "Drystan",
                "Eadbert",
                "Ealdwine",
                "Eddard",
                "Edwyn",
                "Eldred",
                "Emanuel",
                "Esmond",
                "Esmour",
                "Fiebras",
                "Flambard",
                "Foxe",
                "Francis",
                "Frederyk",
                "Fulke",
                "Ganelon",
                "Geoffrey",
                "Gerald",
                "Gerbold",
                "Goddard",
                "Godebert",
                "Gylbart",
                "Gyles",
                "Halstein",
                "Hamon",
                "Heinlein",
                "Hewrey",
                "Higelin",
                "Ivan",
                "Jakys",
                "Jeger",
                "Jeorge",
                "Jonathas",
                "Joseph",
                "Josias",
                "Kain",
                "Kenrick",
                "Ladislas",
                "Laurence",
                "Laurentius",
                "Leavold",
                "Lodwicke",
                "Mansel",
                "Marlowe",
                "Mathye",
                "Morys",
                "Myles",
                "Navarre",
                "Noah",
                "Olyver",
                "Orrick",
                "Oswyn",
                "Parnell",
                "Peter",
                "Powle",
                "Radolf",
                "Randwulf",
                "Reeve",
                "Reinholdt",
                "Reynard",
                "Ribald",
                "Richarde",
                "Ridel",
                "Roger",
                "Samson",
                "Sandre",
                "Sevrin",
                "Symon",
                "Taran",
                "Taylor",
                "Templeton",
                "Tuckard",
                "Tywick",
                "Valentyne",
                "Viktor",
                "Voyce",
                "Vyncent",
                "Wadard",
                "Warin",
                "Werner",
                "Willielmus",
                "Woden",
                "Wolfstan",
                "Xacheus",
                "Ywain",
                "Adela",
                "Admiranda",
                "Aeditha",
                "Aelina",
                "Agnys",
                "Alainne",
                "Aleria",
                "Alyne",
                "Alys",
                "Alyssa",
                "Amelia",
                "Anna",
                "Annabel",
                "Anne",
                "Arlette",
                "Asha",
                "Atilda",
                "Ava",
                "Avelin",
                "Averille",
                "Ayleth",
                "Beatrix",
                "Bertana",
                "Carmen",
                "Cecillia",
                "Cecily",
                "Celes",
                "Celestine",
                "Celestria",
                "Cenota",
                "Chloe",
                "Christabel",
                "Clarimond",
                "Collys",
                "Concessa",
                "Cwengyth",
                "Damaris",
                "Dametta",
                "Decima",
                "Deloys",
                "Diamanda",
                "Dionisia",
                "Dorcas",
                "Edelinne",
                "Eilonwy",
                "Elle",
                "Elsebee",
                "Eltyana",
                "Elyn",
                "Elynor",
                "Elyzabeth",
                "Emblyn",
                "Emeline",
                "Emeny",
                "Emeria",
                "Emilie",
                "Eschina",
                "Estrild",
                "Ethelia",
                "Evelyn",
                "Faye",
                "Frances",
                "Francisca",
                "Garnet",
                "Germainne",
                "Glenda",
                "Gloriana",
                "Gwenneth",
                "Helena",
                "Helenor",
                "Hester",
                "Hilda",
                "Hildegard",
                "Imedia",
                "Ismenia",
                "Jacquette",
                "Jessica",
                "Jocea",
                "Jocelyn",
                "Joleicia",
                "Jolline",
                "Joyse",
                "Judithe",
                "Julia",
                "Juliana",
                "Kath",
                "Katrina",
                "Konstanze",
                "Lauda",
                "Leofwen",
                "Leofwynn",
                "Lyde",
                "Maerwynn",
                "Malin",
                "Margarete",
                "Margeria",
                "Maronne",
                "Martine",
                "Mathild",
                "Melly",
                "Melusine",
                "Meredithe",
                "Merilda",
                "Meryell",
                "Minerva",
                "Morgayne",
                "Muriel",
                "Nicia",
                "Olyffe",
                "Ophellia",
                "Parnell",
                "Patricya",
                "Pelinne",
                "Penelope",
                "Petronilla",
                "Pulmia",
                "Rebecca",
                "Rosa",
                "Rosamund",
                "Sabrine",
                "Samantha",
                "Sarra",
                "Saya",
                "Scarlet",
                "Somerhild",
                "Sylphie",
                "Sylvia",
                "Syndony",
                "Temperance",
                "Tess",
                "Thomasyn",
                "Thora",
                "Tristana",
                "Vega",
                "Wenda",
                "Wulfhilda",
                "Wynefreede",
                "Yve",])
        randomname = random.choice(nameslist)
        nameslist.remove(randomname)

        charclass = random.choice(charclasses)
        randomized_unit = UnitService.create(randomname, charclass, 1, team = team)
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

            del_units = session.query(UnitTable).filter(UnitTable.team >= 1)

            for unit in del_units:
                stmt2 = delete(UnitEquipmentTable).where(UnitEquipmentTable.unit_id == unit.id)
                session.execute(stmt2)
            stmt = delete(UnitTable).where(UnitTable.team >= 1)
            session.execute(stmt)
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

                equipment = self.get_unit_equipment(item.id)

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

                        'weapon_slot1': equipment.get('weapon_slot1', None),
                        'weapon_slot2': equipment.get('weapon_slot2', None),
                        'weapon_slot3': equipment.get('weapon_slot3', None),
                        'helmet_slot': equipment.get('helmet_slot', None),
                        'armor_slot': equipment.get('armor_slot', None),
                        'leg_slot': equipment.get('leg_slot', None),
                        'ring_slot': equipment.get('ring_slot', None),
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
        equipment_list = {}

        with Session(engine) as session:
            equipment = session.query(UnitEquipmentTable).filter(UnitEquipmentTable.unit_id == unit_id).first()
            for key, value in equipment.__dict__.items():
                if "slot" in key:
                    blah = session.query(BaseWeaponTable).get(value)

                    equipment_list.setdefault(key, blah)
        return equipment_list
    
    def refresh_stats_noncombat(unit):

        with Session(engine) as session:

            session.query(UnitTable).filter(UnitTable.id == unit.id).update({'max_hp': 50 + (4 * unit.base_vit)})
            session.query(UnitTable).filter(UnitTable.id == unit.id).update({'current_hp': 50 + (4 * unit.base_vit)})
            session.query(UnitTable).filter(UnitTable.id == unit.id).update({'max_mana': 10 + (2 * unit.base_mnd)})
            session.query(UnitTable).filter(UnitTable.id == unit.id).update({'current_mana': 0})
            session.query(UnitTable).filter(UnitTable.id == unit.id).update({'melee_hit_chance': 70 + round(unit.base_dex / 5)})
            session.query(UnitTable).filter(UnitTable.id == unit.id).update({'ranged_hit_chance': 50 + round(unit.base_dex / 4)})
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

    def update_experience(unit, exp):

        while exp >= 100:
            if unit.level >= 30:
                break
            exp = exp - 100
            UnitService.level_up(unit)
            print(f"{unit.name} leveled up to {unit.level}!")

        with Session(engine) as session:

            session.query(UnitTable).filter(UnitTable.id == unit.id).update({'exp': exp})
            session.commit()
            session.flush()


    def dismiss(unit):

        with Session(engine) as session:
            session.delete(unit)
            stmt = delete(UnitEquipmentTable).where(UnitEquipmentTable.unit_id == unit.id)
            session.execute(stmt)
            session.commit()
            session.flush()

class WeaponService:
    def populate_weapons():

        with Session(engine) as session:

            weapons = [
                {
                    'name': 'Iron Short Sword',
                    'weight': 4, 
                    'value': 50, 
                    'handed': "one-handed", 
                    'damage_type': "Slashing", 
                    'damage_range': 8,
                    'is_ranged': False
                },
                {
                    'name': 'Iron Greatsword',
                    'weight': 8, 
                    'value': 80, 
                    'handed': "two-handed", 
                    'damage_type': "Slashing", 
                    'damage_range': 14,
                    'is_ranged': False
                },
                {
                    'name': 'Iron Rapier',
                    'weight': 3, 
                    'value': 60, 
                    'handed': "one-handed", 
                    'damage_type': "Piercing", 
                    'damage_range': 7,
                    'is_ranged': False
                },
                {
                    'name': 'Iron Morning Star',
                    'weight': 5, 
                    'value': 60, 
                    'handed': "one-handed", 
                    'damage_type': "Crushing", 
                    'damage_range': 6,
                    'is_ranged': False
                },
                {
                    'name': 'Iron Handaxe',
                    'weight': 3, 
                    'value': 40, 
                    'handed': "one-handed", 
                    'damage_type': "Slashing", 
                    'damage_range': 6,
                    'is_ranged': False
                },
                {
                    'name': 'Iron Spear',
                    'weight': 5, 
                    'value': 75, 
                    'handed': "one-handed", 
                    'damage_type': "Piercing", 
                    'damage_range': 6,
                    'is_ranged': False
                },
                {
                    'name': 'Iron Halberd',
                    'weight': 9, 
                    'value': 100, 
                    'handed': "two-handed", 
                    'damage_type': "Slashing", 
                    'damage_range': 8,
                    'is_ranged': False
                },
                {
                    'name': 'Wooden Staff',
                    'weight': 4, 
                    'value': 25, 
                    'handed': "one-handed", 
                    'damage_type': "Crushing", 
                    'damage_range': 4,
                    'is_ranged': False
                },
                {
                    'name': 'Shortbow',
                    'weight': 3, 
                    'value': 50, 
                    'handed': "two-handed", 
                    'damage_type': "Piercing", 
                    'damage_range': 8,
                    'is_ranged': True
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
                    is_ranged=weapon['is_ranged']
                )

                session.add(db_weapon)
            session.commit()


engine = create_engine("sqlite:///database.db", echo=False)
Base.metadata.create_all(engine)