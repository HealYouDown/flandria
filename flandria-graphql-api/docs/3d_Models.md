# 3d Models
Information about the 3d model is stored in the respective `client` file. Most of the models are re-used and just scaled down (for things like Monsters and NPCs).

The code works, but is *a bit* ugly, at least for my liking. Sorry!

## Client structure
Models are stored in multiple different locations in the client:

- `/Actor/Monster` contains all monster models and animations
- `/Actor/NPC/**/` contains all npc models and animations
- `/Actor/User/Item/**` stores all item related models
    - `hef` Explorer Female
    - `hem` Explorer Male
    - `hnf` Noble Female
    - `hnm` Noble Male
    - `hsf` Saint Female
    - `hsm` Saint Male
    - `hwf` Mercenary Female
    - `hwm` Mercenary Male
    - `not` Items like Weapons, Armors, Shields
    - `ground` I **assume** it's base models, as it only contains the male variants of some items. No idea how it's used, we don't care about it.

## Process
(Assumes the models and textures are downloaded to the `tmp` folder)
1. For items, we check for which class and gender we have a model. For monsters and npcs, we don't have to do that.
2. We convert the model to a GLTF file using [Noesis](https://richwhitehouse.com/index.php?content=inc_projects.php&showproject=91) to a temp folder. Noesis creates a splitted GLTF file, so we have to combine it later.
3. If we have a variant, we read the UVs from the generated GLTF file and apply the color to the texture image.
4. We combine the GLTF and write it to our `assets` folder.

## Variants
For hats and dresses, there is a specific column in the `client` file which stores a RGB color value. This value is used at runtime to re-color a certain mesh using the RGB value.
For hats, the mesh used for variants is `hair:2`. For dresses it's `robe:2` (Dresses suprisingly only have robes with variants).

## Noesis
Noesis "just" works, especially with animations. However, some changes were made for it to be useable for florensia models.

File: `lib\noesis\plugins\python\fmt_gamebryo_nif.py`

- Added a `-texture` options to specificy a textures path, otherwise noesis uses the same path as the model.
- Added a `-nif` option which points to the `.nif` model when using `.kf` files (Animations). Otherwise noesis would ask us for a `.nif` file via. windows file dialog.
- If our materials don't have a texture name, we don't render them in the GLTF (Requires `-gltfdiscnoren` flag). Line `#2544`
- A small workaround for realm textures, as they are just weird (or noesis is weird, probably both). Line `#2548`.
