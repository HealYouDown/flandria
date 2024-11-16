from src.database.base import Base
from src.database.mixins import SkillMixin
from src.updater.schema import LoaderInfo


class MonsterSkill(Base, SkillMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_MobSkillAction.bin"],
            client_files=["c_MSkillActionRes.bin"],
            string_files=["MSkillActionStr.dat"],
            description_files=["MobSkillActionDesc.dat"],
        )
    )
