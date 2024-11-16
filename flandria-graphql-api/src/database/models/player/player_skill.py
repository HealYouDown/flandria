import sqlalchemy.orm as orm

from src.database.base import Base
from src.database.mixins import SkillMixin
from src.updater import strategies
from src.updater.schema import LoaderInfo


class PlayerSkill(Base, SkillMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=[
                "s_CharSpellAction.bin",
                "s_CharSkillAction.bin",
                "s_ShipSkillAction.bin",
            ],
            client_files=[
                "c_SpellActionRes.bin",
                "c_SkillActionRes.bin",
                "c_ShipSkillActionRes.bin",
            ],
            string_files=[
                "SpellActionStr.dat",
                "SkillActionStr.dat",
                "ShipSkillActionStr.dat",
            ],
            description_files=[
                "CharSpellActionDesc.dat",
                "CharSkillActionDesc.dat",
                "ShipSkillActionDesc.dat",
            ],
        ),
        loader_strategy=strategies.player_skill,
    )

    required_skills = orm.relationship(
        "PlayerRequiredSkill",
        primaryjoin="foreign(PlayerRequiredSkill.skill_code) == PlayerSkill.code",
        uselist=True,
        cascade="all, delete-orphan",
    )
