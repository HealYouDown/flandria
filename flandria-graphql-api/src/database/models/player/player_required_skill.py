import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.database.base import Base


class PlayerRequiredSkill(Base):
    __table_args__ = (sa.PrimaryKeyConstraint("skill_code", "required_skill_code"),)

    skill_code = orm.mapped_column(
        sa.String(32),
        nullable=False,
        index=True,
    )
    required_skill_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("player_skill.code"),
        index=True,
        nullable=False,
    )
    skill = orm.relationship(
        "PlayerSkill",
        foreign_keys=[required_skill_code],
        uselist=False,
        viewonly=True,
    )
