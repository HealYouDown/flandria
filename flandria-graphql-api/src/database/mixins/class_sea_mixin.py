import sqlalchemy as sa
import sqlalchemy.orm as orm


class ClassSeaMixin:
    is_armored = orm.mapped_column(sa.Boolean, nullable=False, default=False)
    is_big_gun = orm.mapped_column(sa.Boolean, nullable=False, default=False)
    is_torpedo = orm.mapped_column(sa.Boolean, nullable=False, default=False)
    is_maintenance = orm.mapped_column(sa.Boolean, nullable=False, default=False)
    is_assault = orm.mapped_column(sa.Boolean, nullable=False, default=False)
