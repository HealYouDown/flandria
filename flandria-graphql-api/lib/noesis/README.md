# Changes
Changed the kf loading in `plugins\python\fmt_gamebryo_nif.py", line 2566, in kfLoadModel` to use the model name to find the model instead of asking via filedialog

2529 -> workaround for bones showing

## Usage
`noesis.exe ?cmode "models/dodo/lm00202_walk_00.kf" "./out.gltf" -gltfdiscnoren -gltftranscene`

expects a model named `lm00202.nif` next to the `.kf` file.
