import sqlite3

class LevelUpStats:
    def __init__(self, base_str, base_dex, base_spd, base_vit, base_con, base_int, base_mnd, base_res):
        self.base_str = base_str
        self.base_dex = base_dex
        self.base_spd = base_spd
        self.base_vit = base_vit
        self.base_con = base_con
        self.base_int = base_int
        self.base_mnd = base_mnd
        self.base_res = base_res

    def as_dict(self):
        return {
            'base_str': self.base_str,
            'base_dex': self.base_dex,
            'base_spd': self.base_spd,
            'base_vit': self.base_vit,
            'base_con': self.base_con,
            'base_int': self.base_int,
            'base_mnd': self.base_mnd,
            'base_res': self.base_res,
        }

levelup_stats = {
    'Weaponmaster': LevelUpStats(4,2,2,3,2,0,1,0),
    'Elementalist': LevelUpStats(0,1,1,2,0,5,3,2),
    'Rogue': LevelUpStats(1,4,3,2,1,1,2,1),
    'Shaman': LevelUpStats(1,1,2,2,3,1,3,3),
    'Monk': LevelUpStats(2,4,2,2,1,1,1,2),
    'Necromancer': LevelUpStats(0,1,2,1,1,4,4,2),
    'Demonologist': LevelUpStats(2,0,1,2,4,1,3,1),
    'Hemomancer': LevelUpStats(0,1,2,4,1,2,1,3),
    'Astromancer': LevelUpStats(0,1,1,1,1,4,3,4),
    'Crusader': LevelUpStats(3,1,1,2,1,2,1,4),
    'Priest': LevelUpStats(0,0,2,2,1,3,3,3),
                }

charclass_evasion = {
    'Weaponmaster': (0, -10),
    'Elementalist': (0, 10),
    'Rogue': (5, 10),
    'Shaman': (0, 0),
    'Monk': (10, 5),
    'Necromancer': (0, 0),
    'Demonologist': (-10, -10),
    'Hemomancer': (0, 0),
    'Astromancer': (0, 10),
    'Crusader': (-5, -5),
    'Priest': (0, 5),
                }