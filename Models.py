from typing import List
from typing import Any
from typing import Dict
from typing import Type
from typing import Optional
from sqlalchemy import String, select, ForeignKey

from sqlalchemy import create_engine

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

import datetime
import decimal
import uuid

import Unit
import Items
import Stats




class Base(DeclarativeBase):
    pass

class UnitTable(Base):
    __tablename__ = "unit_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    charclass: Mapped[str] = mapped_column(String(30))
    level: Mapped[int] = mapped_column(nullable = True)

    team: Mapped[int] = mapped_column(nullable = True)

    exp: Mapped[int] = mapped_column(nullable = True)

    is_alive: Mapped[bool] = mapped_column(nullable = True)

    base_str: Mapped[int] = mapped_column(nullable = True)
    base_dex: Mapped[int] = mapped_column(nullable = True)
    base_spd: Mapped[int] = mapped_column(nullable = True)
    base_vit: Mapped[int] = mapped_column(nullable = True)
    base_con: Mapped[int] = mapped_column(nullable = True)
    base_int: Mapped[int] = mapped_column(nullable = True)
    base_mnd: Mapped[int] = mapped_column(nullable = True)
    base_res: Mapped[int] = mapped_column(nullable = True)

    current_hp: Mapped[int] = mapped_column(nullable = True)
    max_hp: Mapped[int] = mapped_column(nullable = True)
    current_mana: Mapped[int] = mapped_column(nullable = True)
    max_mana: Mapped[int] = mapped_column(nullable = True)

    melee_hit_chance: Mapped[int] = mapped_column(nullable = True)
    ranged_hit_chance: Mapped[int] = mapped_column(nullable = True)

    base_phys_res: Mapped[int] = mapped_column(nullable = True)
    base_mag_res: Mapped[int] = mapped_column(nullable = True)
    base_evasion: Mapped[int] = mapped_column(nullable = True)

    # weapon_slot1: ?
    # weapon_slot2: ?
    # weapon_slot3: ?
    # helmet_slot: ?
    # armor_slot: ?
    # leg_slot: ?
    # ring_slot: ?

    #def __repr__(self) -> str:
        #return f"{self.unit_id}"

class CharClassTable(Base):
    __tablename__ = "charclass_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    charclass: Mapped[str] = mapped_column(String(30))

class UnitEquipmentTable(Base):
            __tablename__ = "unit_equipment_table"
            id: Mapped[int] = mapped_column(primary_key=True)
            unit_id: Mapped[int] = mapped_column(ForeignKey("unit_table.id"))
            weapon_slot1: Mapped[int] = mapped_column(nullable = True)
            weapon_slot2: Mapped[int] = mapped_column(nullable = True)
            weapon_slot3: Mapped[int] = mapped_column(nullable = True)
            helmet_slot: Mapped[int] = mapped_column(nullable = True)
            armor_slot: Mapped[int] = mapped_column(nullable = True)
            leg_slot: Mapped[int] = mapped_column(nullable = True)
            ring_slot: Mapped[int] = mapped_column(nullable = True)



# class PlayerInventoryTable(Base):
#     __tablename__ = "player_inventory_table"
#     pass


class BaseWeaponTable(Base):
    __tablename__ = "base_weapon_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    weight: Mapped[int] = mapped_column(nullable = True)
    value: Mapped[int] = mapped_column(nullable = True)
    handed: Mapped[str] = mapped_column(String(30))
    damage_type: Mapped[str] = mapped_column(nullable = True)
    damage_range: Mapped[int] = mapped_column(nullable = True)

