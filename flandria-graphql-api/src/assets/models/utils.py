import asyncio
import base64
import os
import struct
from typing import cast

import aiofiles.os as aos
from PIL import Image, ImageDraw
from pygltflib import GLTF2, Accessor, BufferView, Material  # type: ignore

from src.core.constants import NOESIS_PATH

from .exceptions import NoesisConvertException

UV_POINT = tuple[float, float]
UV_TRIANGLE = tuple[UV_POINT, UV_POINT, UV_POINT]


def get_uv_triangles_from_mesh(
    gltf: GLTF2,
    mesh_name: str,
) -> tuple[int, list[UV_TRIANGLE]]:
    for mesh in gltf.meshes:
        # noesis sometimes prefixes our mesh name with objectxxxx_<name>
        if mesh.name is None:
            continue

        is_correct_mesh = mesh.name == mesh_name or mesh.name.endswith(mesh_name)
        if not is_correct_mesh:
            continue

        image_idx = 0
        triangles: list[UV_TRIANGLE] = []
        for primitive in mesh.primitives:
            material: Material = gltf.materials[primitive.material]  # type: ignore
            texcoord: int = material.pbrMetallicRoughness.baseColorTexture.texCoord  # type: ignore
            texcoord_idx = getattr(
                primitive.attributes,
                f"TEXCOORD_{texcoord}",
            )

            # We need the image index later to apply the variant to the image,
            # so why it's ugly, we just return it together with the uvs
            image_idx = cast(int, material.pbrMetallicRoughness.baseColorTexture.index)  # type: ignore

            uvs_accessor: Accessor = gltf.accessors[texcoord_idx]
            uvs_buffer_view: BufferView = gltf.bufferViews[uvs_accessor.bufferView]  # type: ignore
            uvs: list[tuple[float, float]] = get_gltf_data(
                gltf, uvs_buffer_view, uvs_accessor
            )

            indices_accessor: Accessor = gltf.accessors[primitive.indices]  # type: ignore
            indices_buffer_view: BufferView = gltf.bufferViews[
                indices_accessor.bufferView  # type: ignore
            ]
            indices: list[int] = get_gltf_data(
                gltf, indices_buffer_view, indices_accessor
            )

            # in case we ever need the vertex triangles
            # positions_accessor: Accessor = gltf.accessors[primitive.attributes.POSITION]
            # positions_buffer_view: BufferView = gltf.bufferViews[positions_accessor.bufferView]
            # positions = get_gltf_data(gltf, positions_buffer_view, positions_accessor)

            for i in range(0, len(indices), 3):
                uv_triangle = (
                    uvs[indices[i]],
                    uvs[indices[i + 1]],
                    uvs[indices[i + 2]],
                )
                triangles.append(uv_triangle)

        return image_idx, triangles

    raise ValueError(f"Failed to find {mesh_name!r} mesh.")


def get_gltf_data(gltf: GLTF2, buffer_view: BufferView, accessor: Accessor) -> list:
    # FIXME: allow bin files or at least check that it's base64
    base64_string = cast(str, gltf.buffers[buffer_view.buffer].uri)
    base64_data_string = base64_string.split(",")[-1]
    buffer = base64.b64decode(base64_data_string)

    slice = buffer[
        buffer_view.byteOffset : cast(int, buffer_view.byteOffset)
        + buffer_view.byteLength
    ]

    fmt = get_component_format(accessor.componentType)
    if accessor.type == "SCALAR":
        fmt = f"{fmt}"
    if accessor.type == "VEC2":
        fmt = f"<{fmt*2}"
    elif accessor.type == "VEC3":
        fmt = f"<{fmt*3}"
    fmt_size = struct.calcsize(fmt)

    data = []
    offset = 0 + getattr(accessor, "byteOffset", 0)
    for _ in range(accessor.count):
        value: tuple = struct.unpack(fmt, slice[offset : offset + fmt_size])
        if len(value) == 1:
            value = value[0]
        data.append(value)

        offset += fmt_size

    if not len(data) == accessor.count:
        raise ValueError(
            "Somehow we ended up with a mismatch, expected "
            f"{accessor.count} data, got {len(data)}"
        )

    return data


def get_component_format(component_type: int) -> str:
    """Returns the struct format for the given GLTF ComponentType."""
    if component_type == 5120:  # BYTE
        return "b"
    elif component_type == 5121:  # UNSIGNED_BYTE
        return "B"
    elif component_type == 5122:  # SHORT
        return "h"
    elif component_type == 5123:  # UNSIGNED_SHORT
        return "H"
    elif component_type == 5125:  # UNSIGNED_INT
        return "I"
    elif component_type == 5126:  # FLOAT
        return "f"
    else:
        raise ValueError(f"Unknown component type: {component_type}")


def apply_variant_to_gltf(
    gltf: GLTF2,
    tmpdir: str,
    target_color: tuple[int, int, int],
    mesh_name: str,
) -> None:
    image_idx, uv_triangles = get_uv_triangles_from_mesh(gltf, mesh_name)

    texture_name = gltf.images[image_idx].uri
    texture_path = os.path.join(tmpdir, texture_name)

    # Loads the original dds file
    texture_img = Image.open(texture_path)

    # Creates a mask of the hair:2 mesh (from its uv points)
    # using an alphashape.
    mask = Image.new("RGBA", texture_img.size, (0, 0, 0, 0))
    mask_draw = ImageDraw.Draw(mask)

    for triangle in uv_triangles:
        # convert uvs (0.0 - 1.0) to pixel coordinates
        points = [
            (p[0] * texture_img.width, p[1] * texture_img.height) for p in triangle
        ]
        mask_draw.polygon(points, fill=(0, 0, 0, 255), outline=None)

    # Crops the hair:2 uv mesh from the original texture image using the mask
    bg = Image.new("RGBA", texture_img.size, (0, 0, 0, 0))
    uv_part = Image.composite(texture_img, bg, mask)

    # recolors the uv part by blending the target color to it
    uv_part_grayscale = uv_part.convert("L")
    solid_color = Image.new("RGBA", uv_part_grayscale.size, target_color)
    recolored_texture = Image.composite(solid_color, texture_img, uv_part_grayscale)

    recolored_texture.save(texture_path)


async def noesis_convert(src_fpath: str, dst_fpath: str, arguments: list[str]) -> None:
    proc = await asyncio.create_subprocess_exec(
        NOESIS_PATH,
        "?cmode",
        os.path.abspath(src_fpath),
        os.path.abspath(dst_fpath),
        "-gltfdiscnoren",
        "-gltftranscene",
        "-gltfnonoeex",
        *arguments,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    await proc.communicate()

    # We test if the command was successful by checking if a file was created
    # because noesis doesn't know what a returncode, stdout or stderr is -.-
    if not (await aos.path.exists(dst_fpath)):
        raise NoesisConvertException(
            f"Conversion failed for {src_fpath!r} to {dst_fpath!r}"
        )
