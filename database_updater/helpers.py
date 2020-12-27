import itertools
import typing

import requests
from database_updater.constants import PATCHSERVER_URL
from database_updater.model_lists import MODELS


def join_url(*parts) -> str:
    """Joins url parts.

    Returns:
        str: URL.
    """
    return "/".join(parts)


def get_filenames_for_models() -> typing.List[str]:
    """Returns a list with all filenames that are defined
    inside the models. Those *have* to be there, otherwise
    a database cannot be created.

    Raises:
        AttributeError: _mapper_utils is not defined in the model.
        KeyError: files is not defined inside _mapper_utils.

    Returns:
        typing.List[str]: List with all filenames that are needed to
            create the database.
    """
    filenames = []

    for model in MODELS:
        # Check if _mapper_utils and files are defined
        if not hasattr(model, "_mapper_utils"):
            raise AttributeError(f"Model {model} is missing _mapper_utils.")

        if "files" not in model._mapper_utils:
            raise KeyError((f"Model {model} is missing files implementation "
                            "in _mapper_utils."))

        # Update filenames with all filenames from 'server', 'client',
        # ... keys
        filenames.extend(itertools.chain.from_iterable(
            model._mapper_utils["files"].values()))

    return filenames


def get_patchserver_file_urls() -> typing.List[str]:
    """Returns a list with all urls that have to be downloaded
    to be able to create a database.

    Returns:
        typing.List[str]: List with urls to the patchserver.
    """
    # version.bin url which contains all files inside the florensia
    # client: http://patch.florensia-online.eu/LIVE/Patch/Update/version.bin
    url = join_url(PATCHSERVER_URL, "version.bin")

    # Request file and decode its content
    with requests.get(url) as req:
        if req.status_code != 200:
            raise Exception(("HTTP request to patchserver "
                             f"failed with {req.status_code}"))
        content = req.content.decode("euc_kr")

    # Split the content into lines and remove the first one
    # as it does not contain any useful information.
    lines = content.splitlines()[1:]

    # Get all filenames that are needed for models
    model_filenames = get_filenames_for_models()

    # Filter lists with unneeded icon/texture files for monster, npc and item
    # icons.
    excluded_monsters = ["Textures", "Textures_low"]

    excluded_npcs = ["Textures_low", "Textures", "Monster", "Guildwar"]

    excluded_items = ["emotion", "abn.png", "asn.png", "ccf.png",
                      "cre.png", "emb.png", "emoticonlist.png",
                      "fla.png", "isp.png", "isr.png", "ist.png",
                      "isw.png"]

    # We want to download all files that are neeed for models as
    # well as all icons that we need. This excludes some other
    # urls, which we filter out.
    urls = []

    for line in lines:
        # Example line:
        # Bin/Setting/ChattingSystem.ini| 30160448 2030885142 544
        fpath, fname = line.split("| ")[0].rsplit("/", maxsplit=1)
        fpath_parts = fpath.split("/")

        if fpath.startswith("Data/DataTable"):
            # Filter out all DataTables except ClientTable, ServerTable
            # StringTable and QuestData.
            if fpath_parts[2] not in ["ClientTable", "ServerTable",
                                      "StringTable", "QuestData"]:
                continue

            # Filter out all Client/Server/String Table files that are not
            # needed for models.
            # QuestData is not filtered.
            if fpath_parts[2] != "QuestData":
                if fname not in model_filenames:
                    continue

        elif fpath.startswith("Data/Actor/Monster"):
            if not fname.endswith(".png"):
                continue

            if any(exclude in fpath_parts
                   for exclude in excluded_monsters):
                continue

        elif fpath.startswith("Data/Actor/NPC"):
            if not fname.endswith(".png"):
                continue

            if any(exclude in fpath_parts
                   for exclude in excluded_npcs):
                continue

            # Filter out npc banner images
            if fname.startswith("p_"):
                continue

        elif fpath.startswith("Data/UI/Icon"):
            if not fname.endswith(".png"):
                continue

            if any(exclude in fpath_parts
                   for exclude in excluded_items):
                continue

        else:
            # Well, we don't want anything else!
            continue

        # No filters matched the path, so we create a url and add it
        # to the list.
        urls.append(join_url(PATCHSERVER_URL, *fpath_parts, f"{fname}.zip"))

    return urls
