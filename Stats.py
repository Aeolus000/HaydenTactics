
class LevelUpStats:
    def __init__(self, baseStrength, baseDexterity, baseSpeed, baseVitality, baseConstitution, baseIntelligence, baseMind, baseResistance):
        self.baseStrength = baseStrength
        self.baseDexterity = baseDexterity
        self.baseSpeed = baseSpeed
        self.baseVitality = baseVitality
        self.baseConstitution = baseConstitution
        self.baseIntelligence = baseIntelligence
        self.baseMind = baseMind
        self.baseResistance = baseResistance

    def as_dict(self):
        return {
            'baseStrength': self.baseStrength,
            'baseDexterity': self.baseDexterity,
            'baseSpeed': self.baseSpeed,
            'baseVitality': self.baseVitality,
            'baseConstitution': self.baseConstitution,
            'baseIntelligence': self.baseIntelligence,
            'baseMind': self.baseMind,
            'baseResistance': self.baseResistance,
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