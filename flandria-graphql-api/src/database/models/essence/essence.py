import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.core.enums import EssenceEquipType
from src.database.base import Base
from src.database.mixins import BaseMixin, EffectMixin
from src.updater.schema import ColumnInfo, LoaderInfo


class Essence(Base, BaseMixin, EffectMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_ArtifactItem.bin"],
            client_files=["c_ArtifactRes.bin"],
            string_files=["ArtifactStr.dat"],
        ),
        include_in_itemlist=True,
    )

    equip_type = orm.mapped_column(
        sa.Enum(EssenceEquipType),
        nullable=False,
        doc=(
            "Equip type (what piece) for the essence, "
            "like all, armor, only weapons ..."
        ),
        info=ColumnInfo(
            key="장착대상",
            transforms=[lambda v: EssenceEquipType(v)],
        ),
    )
    required_level = orm.mapped_column(
        sa.Integer,
        nullable=False,
        doc="Weapon level required to put the essence on",
        info=ColumnInfo(key="육상LV"),
    )
    is_core = orm.mapped_column(
        sa.Boolean,
        nullable=False,
        doc="Whether the essence is for core slots only",
        info=ColumnInfo(key="AtI타입"),
    )

    # TODO: Figure out formular for essence applying cost
    # BUG: right now the cost is different for client and server (20.05.2024 - Jeremy)
    # Mounting cost 고정비용
    # Mounting Item Level Cost LV비용
    # Mounting Unit Cost 비용단위
