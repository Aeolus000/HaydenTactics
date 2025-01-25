from typing import List
from typing import Any
from typing import Dict
from typing import Type
from typing import Optional
from sqlalchemy import String, Boolean, select, ForeignKey, JSON

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
    base_phys_evasion: Mapped[int] = mapped_column(nullable = True)
    base_mag_evasion: Mapped[int] = mapped_column(nullable = True)

    # ability1: Mapped[JSON] = mapped_column(nullable = True)
    # ability2: Mapped[JSON] = mapped_column(nullable = True)
    # ability3: Mapped[JSON] = mapped_column(nullable = True)
    # ability4: Mapped[JSON] = mapped_column(nullable = True)

class CharClassTable(Base):
    __tablename__ = "charclass_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    charclass: Mapped[str] = mapped_column(String(30))


class PlayerInventoryTable(Base):
    __tablename__ = "playerinv_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_type: Mapped[str] = mapped_column(nullable = False)
    quantity: Mapped[int] = mapped_column(nullable = False)
    item_id: Mapped[int] = mapped_column()
    

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

class BaseWeaponTable(Base):
    __tablename__ = "base_weapon_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    weight: Mapped[int] = mapped_column(nullable = True)
    value: Mapped[int] = mapped_column(nullable = True)
    handed: Mapped[str] = mapped_column(String(30))
    damage_type: Mapped[str] = mapped_column(nullable = True)
    damage_range: Mapped[int] = mapped_column(nullable = True)
    is_ranged: Mapped[bool] = mapped_column(unique = False, default = False)

class BaseArmorTable(Base):
    __tablename__ = "base_armor_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    weight: Mapped[int] = mapped_column(nullable = True)
    value: Mapped[int] = mapped_column(nullable = True)

class AbilityTable(Base):
    __tablename__ = "ability_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    charclass: Mapped[str] = mapped_column(String(30))
    mana_cost: Mapped[int] = mapped_column(nullable = True)
    hp_cost: Mapped[int] = mapped_column(nullable = True)
    action_cost: Mapped[int] = mapped_column(nullable = True)
    target_type: Mapped[int] = mapped_column(nullable = True)
    area_effect: Mapped[int] = mapped_column(nullable = True)
    damage: Mapped[int] = mapped_column(nullable = True)
    damage_element: Mapped[int] = mapped_column(nullable = True)
      
