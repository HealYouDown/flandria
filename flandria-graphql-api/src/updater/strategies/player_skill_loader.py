from typing import TYPE_CHECKING

from src.updater.file_data import FileData
from src.updater.helpers import (
    get_class_land,
    get_class_sea,
    get_effects,
    get_required_skills,
    map_row_to_model,
)

if TYPE_CHECKING:
    from src.database.types import ModelCls
    from src.updater.schema import LoaderInfo

    from .types import T_STRATEGY_RETURN


def player_skill(
    model_cls: "ModelCls",
    loader_info: "LoaderInfo",
) -> "T_STRATEGY_RETURN":
    from src.database.models import Effect, PlayerRequiredSkill

    data = FileData.from_files(loader_info.files)

    skills: list[dict] = []
    required_skills: list[dict] = []
    effects: list[dict] = []

    for row in data.server_data:
        pk, skill = map_row_to_model(model_cls, row, data)
        skill.update(get_class_land(row, "player_skill"))
        skill.update(get_class_sea(row, "player_skill"))

        skills.append(skill)
        required_skills.extend(get_required_skills(row, pk))
        effects.extend(get_effects(row, "player_skill", pk))

    return [
        (model_cls, skills),
        (PlayerRequiredSkill, required_skills),
        (Effect, effects),
    ]
