from typing import TYPE_CHECKING

from src.updater.file_data import FileData
from src.updater.helpers import map_row_to_model

if TYPE_CHECKING:
    from src.database.types import ModelCls
    from src.updater.schema import LoaderInfo

    from .types import T_STRATEGY_RETURN


def recipe(
    model_cls: "ModelCls",
    loader_info: "LoaderInfo",
) -> "T_STRATEGY_RETURN":
    from src.database.models import RecipeRequiredMaterial

    data = FileData.from_files(loader_info.files)

    recipes: list[dict] = []
    required_materials: list[dict] = []
    for row in data.server_data:
        pk, obj = map_row_to_model(model_cls, row, data)

        for i in range(1, 7):
            material_code = row[f"재료{i}"]
            quantity = row[f"필요량{i}"]

            if material_code is not None:
                required_materials.append(
                    {
                        "recipe_code": pk,
                        "material_code": material_code,
                        "quantity": quantity,
                    }
                )

        recipes.append(obj)

    return [
        (model_cls, recipes),
        (RecipeRequiredMaterial, required_materials),
    ]
