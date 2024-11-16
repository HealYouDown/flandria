import os

PATCHSERVER_URL = r"http://patch.florensia-online.eu/LIVE/Patch/Update"

NOESIS_PATH = os.path.abspath("lib/noesis/Noesis64.exe")

# The language to use when extracting names, descriptions and the likes
LANGUAGE = "English"

# Fallbacks to use if no data is found
FALLBACK_NAME = "NO NAME"
FALLBACK_ACTOR_ICON = "npcface.png"
FALLBACK_ITEM_ICON = "def_255.png"
FALLBACK_SKILL_ICON = "def_255.png"

# Path to the stats file for all base classes
STATS_DATA_PATH = os.path.join("data", "stats")

# Temporary paths to store all data that is used to update the database
TMP_PATH = "tmp"
UPDATER_DATA_PATH = os.path.join(TMP_PATH, "data")
DROPS_DATA_PATH = os.path.join(TMP_PATH, "drops")
MAPS_DATA_PATH = os.path.join(TMP_PATH, "maps")
ICONS_DATA_PATH = os.path.join(TMP_PATH, "icons")

MODELS_DATA_PATH = os.path.join(TMP_PATH, "models")

# Output folder for generated assets
OUTPUT_ASSETS_FOLDER = "assets"
