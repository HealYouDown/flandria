import asyncio
import os
import tempfile
import warnings
from typing import Literal, Optional, cast

import aiofiles.os as aos
from loguru import logger
from pygltflib import GLTF2, BufferFormat, ImageFormat  # type: ignore

from src.assets.models import KFMFile
from src.assets.models.utils import apply_variant_to_gltf, noesis_convert
from src.core.constants import MODELS_DATA_PATH, OUTPUT_ASSETS_FOLDER
from src.database.column_types.rgb import rgb_to_int

from .exceptions import NoesisConvertException


async def convert_actor_model(
    sempahore: asyncio.Semaphore,
    actor_type: Literal["monster"] | Literal["npc"],
    model_name: str,
):
    async with sempahore:
        # Folder with the .nif file as well as all keyframe animations
        src_path = os.path.join(MODELS_DATA_PATH, actor_type, model_name)
        if not (await aos.path.exists(src_path)):
            logger.error(f"Model data for {model_name!r} does not exist, skipping")
            return

        # Textures path
        textures_path = os.path.join(MODELS_DATA_PATH, actor_type, "Textures_low")

        # Folder to export models to after post-convert process
        output_assets_path = os.path.join(
            OUTPUT_ASSETS_FOLDER, "models", actor_type, model_name
        )
        if not (await aos.path.exists(output_assets_path)):
            await aos.makedirs(output_assets_path, exist_ok=True)

        try:
            kfm_filename = next(
                filename
                for filename in (await aos.listdir(src_path))
                if filename.endswith(".kfm")
            )
        except Exception as e:
            logger.error(f"Failed to find kfm file: {e!r}, skipping")
            return

        # We first convert all .nif models to .gltf using noesis
        # We then have to combine all files from the gltf together (as noesis can't do that)
        with tempfile.TemporaryDirectory() as tmpdir:
            kfm = KFMFile.read(os.path.join(src_path, kfm_filename))

            for kf_filename in kfm.animations:
                logger.info(f"Converting {model_name!r} - {kf_filename!r}")

                kf_filepath = os.path.join(src_path, kf_filename)
                out_filename, _ = os.path.splitext(kf_filename)

                tmp_dst_fpath = os.path.join(tmpdir, f"{out_filename}.gltf")

                try:
                    await noesis_convert(
                        kf_filepath,
                        tmp_dst_fpath,
                        arguments=[
                            "-nif",
                            kfm.nif_filename,
                            "-textures",
                            textures_path,
                        ],
                    )
                except NoesisConvertException as e:
                    logger.error(str(e))
                    continue

                # GLTF technically supports multiple animations, but we would have to
                # transform a lot of shit, just adding animation samplers doesn't work :(
                with warnings.catch_warnings(action="ignore"):
                    try:
                        gltf = cast(GLTF2, GLTF2().load(tmp_dst_fpath))
                    except Exception as e:
                        logger.error(
                            f"Failed to load gltf file {tmp_dst_fpath!r}: {e!r}, skipping"
                        )
                        continue
                    gltf.convert_buffers(BufferFormat.DATAURI)
                    gltf.convert_images(ImageFormat.DATAURI)
                    gltf.save(os.path.join(output_assets_path, f"{out_filename}.gltf"))


async def convert_weapon_model(
    sempahore: asyncio.Semaphore,
    model_name: str,
):
    async with sempahore:
        model_fpath = os.path.join(
            MODELS_DATA_PATH, "items", "item_not", f"item_not_{model_name}.nif"
        )
        if not (await aos.path.exists(model_fpath)):
            logger.error(f"Model data for {model_name!r} does not exist, skipping")
            return

        textures_path = os.path.join(
            MODELS_DATA_PATH, "items", "item_not", "Textures_low"
        )

        output_assets_path = os.path.join(OUTPUT_ASSETS_FOLDER, "models", "weapon")
        if not (await aos.path.exists(output_assets_path)):
            await aos.makedirs(output_assets_path, exist_ok=True)

        with tempfile.TemporaryDirectory() as tmpdir:
            logger.info(f"Converting {model_name!r}")
            tmp_dst_fpath = os.path.join(tmpdir, f"{model_name}.gltf")

            try:
                await noesis_convert(
                    model_fpath,
                    tmp_dst_fpath,
                    arguments=[
                        "-textures",
                        textures_path,
                    ],
                )
            except NoesisConvertException as e:
                logger.error(str(e))
                return

            with warnings.catch_warnings(action="ignore"):
                try:
                    gltf = cast(GLTF2, GLTF2().load(tmp_dst_fpath))
                except Exception as e:
                    logger.error(
                        f"Failed to load gltf file {tmp_dst_fpath!r}: {e!r}, skipping"
                    )
                    return
                gltf.convert_buffers(BufferFormat.DATAURI)
                gltf.convert_images(ImageFormat.DATAURI)
                gltf.save(os.path.join(output_assets_path, f"{model_name}.gltf"))


async def convert_class_and_gender_model(
    sempahore: asyncio.Semaphore,
    model_name: str,
    out_path_prefix: str,
    variant: Optional[tuple[int, int, int]] = None,
    variant_mesh_name: Optional[str] = None,
) -> None:
    async with sempahore:
        key_mapping = {
            "hef": ("explorer", "female"),
            "hem": ("explorer", "male"),
            "hnf": ("noble", "female"),
            "hnm": ("noble", "male"),
            "hsf": ("saint", "female"),
            "hsm": ("saint", "male"),
            "hwf": ("mercenary", "female"),
            "hwm": ("mercenary", "male"),
            "not": ("all", "genderless"),
        }

        model_fpaths: list[tuple[str, str, str]] = []
        for key in key_mapping:
            model_path = os.path.join(
                MODELS_DATA_PATH, "items", f"item_{key}", f"item_{key}_{model_name}.nif"
            )
            if not (await aos.path.exists(model_path)):
                continue

            textures_path = os.path.join(
                MODELS_DATA_PATH, "items", f"item_{key}", "Textures_low"
            )

            model_fpaths.append((key, model_path, textures_path))

        if not model_fpaths:
            logger.error(f"No model data for {model_name!r} found, skipping")
            return

        with tempfile.TemporaryDirectory() as tmpdir:
            logger.info(f"Converting {model_name!r}")

            for key, model_fpath, textures_path in model_fpaths:
                tmp_subdir = os.path.join(tmpdir, key)
                await aos.makedirs(tmp_subdir, exist_ok=True)

                tmp_dst_fpath = os.path.join(tmp_subdir, f"{model_name}.gltf")

                try:
                    await noesis_convert(
                        model_fpath,
                        tmp_dst_fpath,
                        arguments=[
                            "-textures",
                            textures_path,
                        ],
                    )
                except NoesisConvertException as e:
                    logger.error(f"Failed to convert {key}-{model_name}: {str(e)})")
                    continue

                with warnings.catch_warnings(action="ignore"):
                    try:
                        gltf = cast(GLTF2, GLTF2().load(tmp_dst_fpath))
                    except Exception as e:
                        logger.error(
                            f"Failed to load gltf file {tmp_dst_fpath!r}: {e!r}, skipping"
                        )
                        return
                    gltf.convert_buffers(BufferFormat.DATAURI)

                    if variant is not None:
                        assert variant_mesh_name is not None

                        try:
                            apply_variant_to_gltf(
                                gltf,
                                tmp_subdir,
                                variant,
                                variant_mesh_name,
                            )
                        except Exception as e:
                            logger.error(
                                f"Failed to apply variant {variant!r} to {key}-{model_name}: {e!r}, skipping"
                            )
                            continue
                        model_folder_name = f"{model_name}_{rgb_to_int(variant)}"
                    else:
                        model_folder_name = model_name

                    gltf.convert_images(ImageFormat.DATAURI)

                    out_path = os.path.join(
                        OUTPUT_ASSETS_FOLDER,
                        "models",
                        out_path_prefix,
                        model_folder_name,
                        *key_mapping[key],
                    )
                    await aos.makedirs(out_path, exist_ok=True)
                    gltf.save(os.path.join(out_path, f"{model_name}.gltf"))
