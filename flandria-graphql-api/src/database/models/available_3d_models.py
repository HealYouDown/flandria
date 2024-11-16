import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.core import enums
from src.database.base import Base
from src.database.column_types import RGB


class Available3DModel(Base):
    __table_args__ = (sa.Index("model_idx", "model_name", "model_variant"),)

    asset_path = orm.mapped_column(sa.String, primary_key=True)
    filename = orm.mapped_column(sa.String, nullable=False)

    model_name = orm.mapped_column(sa.String, nullable=False)
    model_variant = orm.mapped_column(RGB, nullable=True)

    animation_name = orm.mapped_column(sa.String, nullable=True)
    character_class = orm.mapped_column(sa.Enum(enums.Model3DClass), nullable=True)
    gender = orm.mapped_column(sa.Enum(enums.Model3DGender), nullable=True)
