from typing import List
from typing import Any
from typing import Dict
from typing import Type
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String

from sqlalchemy import create_engine

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

import datetime
import decimal
import uuid


engine = create_engine("sqlite://", echo=True)

class Base(DeclarativeBase):
    pass

class Unit(Base):
    __tablename__ = "unit"

    unit_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    charclass: Mapped[str] = mapped_column(String(30))
    level: Mapped[int] = mapped_column

    initiative: Mapped[int] = mapped_column
    exp: Mapped[int] = mapped_column

    base_str: Mapped[int] = mapped_column
    base_dex: Mapped[int] = mapped_column
    base_spd: Mapped[int] = mapped_column
    base_vit: Mapped[int] = mapped_column
    base_con: Mapped[int] = mapped_column
    base_int: Mapped[int] = mapped_column
    base_mnd: Mapped[int] = mapped_column
    base_res: Mapped[int] = mapped_column

    current_hp: Mapped[int] = mapped_column
    max_hp: Mapped[int] = mapped_column
    current_mana: Mapped[int] = mapped_column
    max_mana: Mapped[int] = mapped_column

    melee_hit_chance: Mapped[int] = mapped_column
    ranged_hit_chance: Mapped[int] = mapped_column

    base_phys_res: Mapped[int] = mapped_column
    base_mag_res: Mapped[int] = mapped_column
    base_evasion: Mapped[int] = mapped_column

    # weapon_slot1: ?
    # weapon_slot2: ?
    # weapon_slot3: ?
    # helmet_slot: ?
    # armor_slot: ?
    # leg_slot: ?
    # ring_slot: ?



