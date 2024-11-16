from src.database.base import Base
from src.database.mixins import SkillMixin
from src.updater.schema import LoaderInfo


class PetSkill(Base, SkillMixin):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            server_files=["s_PetSkillAction.bin"],
            client_files=["c_PetSkillActionRes.bin"],
            string_files=["PetSkillActionStr.dat"],
            description_files=["PetSkillActionDesc.dat"],
        )
    )
