import sqlalchemy as sa
import sqlalchemy.orm as orm


class ClassLandMixin:
    is_noble = orm.mapped_column(sa.Boolean, nullable=False, default=False)
    is_court_magician = orm.mapped_column(sa.Boolean, nullable=False, default=False)
    is_magic_knight = orm.mapped_column(sa.Boolean, nullable=False, default=False)

    is_saint = orm.mapped_column(sa.Boolean, nullable=False, default=False)
    is_priest = orm.mapped_column(sa.Boolean, nullable=False, default=False)
    is_shaman = orm.mapped_column(sa.Boolean, nullable=False, default=False)

    is_mercenary = orm.mapped_column(sa.Boolean, nullable=False, default=False)
    is_gladiator = orm.mapped_column(sa.Boolean, nullable=False, default=False)
    is_guardian_swordsman = orm.mapped_column(sa.Boolean, nullable=False, default=False)

    is_explorer = orm.mapped_column(sa.Boolean, nullable=False, default=False)
    is_excavator = orm.mapped_column(sa.Boolean, nullable=False, default=False)
    is_sniper = orm.mapped_column(sa.Boolean, nullable=False, default=False)
