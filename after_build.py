"""
This file is run after a successfull build of the frontend.

Moves files etc. to the correct directories and gzips js.
"""

import gzip
import os
import json
import shutil
from distutils.dir_util import copy_tree
import sys

root_dir = os.path.abspath(os.path.dirname(__file__))
build_folder = os.path.join(root_dir, "flandria-frontend", "build")

with open(os.path.join(build_folder, "asset-manifest.json"), "r") as fp:
    manifest = json.load(fp)

templates_folder = os.path.join(root_dir, "webapp", "templates")
static_folder = os.path.join(root_dir, "webapp", "static")

# Copy html to templates folder
shutil.copyfile(os.path.join(build_folder, "index.html"),
                os.path.join(templates_folder, "index.html"))

# Copy favicon
shutil.copyfile(os.path.join(build_folder, "favicon.ico"),
                os.path.join(static_folder, "favicon.ico"))

# Copy assets
copy_tree(os.path.join(build_folder, "assets"),
          os.path.join(static_folder, "assets"))

# Copy css
copy_tree(os.path.join(build_folder, "static", "css"),
          os.path.join(static_folder, "css"))

# Create js folder in static
if not os.path.exists(os.path.join(static_folder, "js")):
    os.mkdir(os.path.join(static_folder, "js"))

for fpath in manifest["entrypoints"]:
    if not fpath.endswith("js"):
        continue

    fname = fpath.rsplit("/", 1)[-1]

    # Copy normal js file
    shutil.copyfile(
        os.path.join(build_folder, "static", "js", fname),
        os.path.join(static_folder, "js", fname))

    with open(os.path.join(
        build_folder, "static", "js", fname), "rb"
    ) as fp:

        # Write original content to gzipped file
        gz_main_js = gzip.GzipFile(
            os.path.join(static_folder, "js", f"{fname}.gz"),
            "w")

        gz_main_js.write(fp.read())
