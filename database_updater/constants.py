import os

DATABASE_UPDATER_FPATH = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(DATABASE_UPDATER_FPATH, os.pardir))

# Patchserver URL
PATCHSERVER_URL = r"http://patch.florensia-online.eu/LIVE/Patch/Update"

# Temp folder to download files to
TEMP_FOLDER = os.path.join(
    DATABASE_UPDATER_FPATH,
    "temp"
)
QUESTS_FOLDER = os.path.join(TEMP_FOLDER, "quests")

PALETTES_FOLDER = os.path.join(TEMP_FOLDER, "palettes")

PERSISTENT_DATA_FOLDER = os.path.join(DATABASE_UPDATER_FPATH, "persistent_data")

# Create folders they do not exist
if not os.path.exists(TEMP_FOLDER):
    os.mkdir(TEMP_FOLDER)

if not os.path.exists(QUESTS_FOLDER):
    os.mkdir(QUESTS_FOLDER)

if not os.path.exists(PALETTES_FOLDER):
    os.mkdir(PALETTES_FOLDER)

PUBLIC_ASSETS_FOLDER = os.path.join(
    ROOT_DIR, "flandria-frontend", "public", "assets")

# Language to use for descriptions, names etc.
LANGUAGE = "English"
