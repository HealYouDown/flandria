import os

from loguru import logger

from src.core.enums import Model3DClass, Model3DGender
from src.database.column_types.rgb import int_to_rgb
from src.database.engine import Session
from src.database.models import Available3DModel

ASSETS_PREFIX = ("assets", "models")


def parse_animation_name(filename: str) -> str:
    name, _ = os.path.splitext(filename)

    try:
        parts = name.split("_")
        assert len(parts) >= 2

        name, num = parts[-2::]
        num = int(num)

        return f"{name} ({num})"

    except Exception:
        logger.debug(f"Failed to parse animation name for {name!r}")
        return name


def parse_actors(key: str, path: str) -> list[Available3DModel]:
    models = []

    for model_code in os.listdir(path):
        model_folder = os.path.join(path, model_code)
        for model_animation_filename in os.listdir(model_folder):
            animation_name = parse_animation_name(model_animation_filename)
            asset_path = "/" + "/".join(
                (
                    *ASSETS_PREFIX,
                    key,
                    model_code,
                    model_animation_filename,
                )
            )
            models.append(
                Available3DModel(
                    asset_path=asset_path,
                    filename=model_animation_filename,
                    model_name=model_code,
                    animation_name=animation_name,
                )
            )

    return models


def parse_weapon(key: str, path: str) -> list[Available3DModel]:
    models = []

    for filename in os.listdir(path):
        model_code, _ = os.path.splitext(filename)
        asset_path = "/" + "/".join((*ASSETS_PREFIX, key, filename))
        models.append(
            Available3DModel(
                asset_path=asset_path,
                filename=filename,
                model_name=model_code,
            )
        )

    return models


def parse_extra_equipment(key: str, path: str) -> list[Available3DModel]:
    models = []

    for model_code_variant_folder_name in os.listdir(path):
        # variant models have <code>_<variant> as the folder name
        try:
            model_code, variant = model_code_variant_folder_name.split("_")
            variant = int_to_rgb(int(variant))
        except ValueError:
            model_code = model_code_variant_folder_name
            variant = None

        model_root_folder = os.path.join(path, model_code_variant_folder_name)
        for class_name in os.listdir(model_root_folder):
            class_folder_path = os.path.join(model_root_folder, class_name)
            class_ = getattr(Model3DClass, class_name.upper())
            for gender_name in os.listdir(class_folder_path):
                gender = getattr(Model3DGender, gender_name.upper())
                filename = f"{model_code}.gltf"
                asset_path = "/" + "/".join(
                    (
                        *ASSETS_PREFIX,
                        key,
                        model_code_variant_folder_name,
                        class_name,
                        gender_name,
                        filename,
                    )
                )

                models.append(
                    Available3DModel(
                        asset_path=asset_path,
                        filename=filename,
                        model_name=model_code,
                        model_variant=variant,
                        character_class=class_,
                        gender=gender,
                    )
                )

    return models


def load_available_3d_models(model_asset_folder: str) -> None:
    models: list[Available3DModel] = []

    for key in os.listdir(model_asset_folder):
        path = os.path.join(model_asset_folder, key)
        logger.info(f"Loading {key} models...")

        if key in ("armor", "dress", "hat"):
            models.extend(parse_extra_equipment(key, path))

        elif key in ("monster", "npc"):
            models.extend(parse_actors(key, path))

        elif key in ("weapon",):
            models.extend(parse_weapon(key, path))

        else:
            raise ValueError(f"Unknown folder in models: {key!r}")

    with Session() as session:
        session.query(Available3DModel).delete(synchronize_session=False)

        session.add_all(models)
        session.commit()
