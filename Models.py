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
    #unit_id: Mapped[int] = mapped_column()
    name: Mapped[str] = mapped_column(String(30))
    charclass: Mapped[str] = mapped_column(String(30))
    level: Mapped[int] = mapped_column(nullable = True)

    initiative: Mapped[int] = mapped_column(nullable = True)
    exp: Mapped[int] = mapped_column(nullable = True)
    action_points: Mapped[int] = mapped_column(nullable = True)

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




# unit = Unit.Unit("Hayden", "Shaman", 1)

#unit_list = Unit.unit_list

# with Session(engine) as session:

#     unit1 = UnitTable(
#         unit_id=unit.unit_id,
#         name=unit.name,
#         charclass=unit.charclass,
#         level=unit.level,
#         base_str=unit.base_str,
#         base_dex=unit.base_dex,
    # )
    # unit = Unit(
    #     unit_id=1,
    #     name="Hayden",
    #     charclass="Weaponmaster",
    #     level=1,
    # )
    # unit2 = Unit(
    #     unit_id=2,
    #     name="Jessica",
    #     charclass="Elementalist",
    #     level=1,
    # )

    #session.add_all([unit, unit2])
    # session.add(unit1)

    # session.commit()


    # #stmt = select(UnitTable).where(UnitTable.id >= 1)
    # result = session.execute(select(UnitTable).order_by(UnitTable.id))


    # print(result.all())

    # print(unit1.name)

    #selected_unit = result.all()[0]
    #print(selected_unit.name)
    #print(UnitTable.query.all())