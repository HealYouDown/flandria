from webapp.extensions import db
from webapp.models.custom_sql_classes import CustomColumn
from database_updater.constants import LANGUAGE

MAP_CODE_TO_LTWH = {
    "AC1_000": "-23403.838,16432.385,43000,43000",  # Roxbury
    "AF1_000": "-40190.055,14851.078,72000,72000",  # Larks
    "AF2_000": "-63875.937, 62559.402, 110000, 110000",  # Weed
    "AD1_000": "-26359.74,22704.572,54000,54000",  # Mine
    "AD2_000": "11914.102, 54492.973, 75000, 75000",  # Fox Den
    "AD3_000": "-26359.74,22704.572,54000,54000",  # Labo
    "AD4_000": "11914.102, 54492.973, 75000, 75000",  # Elite Fox Den
    "AD5_000": "-26359.74,22704.572,54000,54000",  # Elite Mine
    "DF1_000": "-72943.6,69344.6,97999.31,87514.5",  # Realm

    "BC1_000": "-27912.443,22487.713,58000,58000",  # Castle Hall
    "BF1_000": "-87959.516,69603.398,112700,112700",  # Castle Field
    "BF2_000": "-46751.25, 64504.289, 100000, 100000",  # Lava Plateau
    "BD1_000": "-29600.158,51421.5,62999.998,62999.998",  # Tulach #1
    "BD2_000": "-34428.188,38847.508,68000,68000",  # Tulach #2
    "BD3_000": "-37810.672,38718.746,77000,77000",  # Tulach #3

    "CC1_000": "-13384.699,10326.811,27500,27500",  # Glostern
    "CF1_000": "-40510.512,22337.574,90000,90000",  # Gloshire

    "SD1_000": "-108493.789,119034.508,220000,220000",  # Sea of Bone
    "SD2_000": "-157716.73, 221279.75, 370000, 370000",  # Dragon Base
    "SD1F1_000": "-22249.564,22064.955,42000,42000",  # Peregrine Falcon..
    "SD2F1_000": "-47675.336,50207.309,97000,97000",  # Hidden Port

    "CD1_000": "-39584.227,39928.434,81000,81000",  # 1st Basement Ave
    "CD2_000": "-39584.227,39928.434,81000,81000",  # 2nd Basement Ave
    "CD3_000": "-56246.219, 57060.84, 115000, 115000",  # 3rd Basement Ave
    "CD4_000": "-38540.516,38098.32,80000,80000",  # Room of Pain
    "CD5_000": "-38540.516,38098.32,80000,80000",  # Laboratory of Death
    "CD6_000": "-38540.367, 43846.922, 80000, 80000",  # Laboratory of Blood

    "CED1_000": "-39584.227,39928.434,81000,81000",  # Elite Ave...
    "CED2_000": "-39584.227,39928.434,81000,81000",
    "CED3_000": "-56246.219, 57060.84, 115000, 115000",
    "CED4_000": "-38540.516,38098.32,80000,80000",
    "CED5_000": "-38540.516,38098.32,80000,80000",
    "CED6_000": "-38540.367, 43846.922, 80000, 80000",

    "EC1_000": "-17378.777,17133.637,40000,40000",  # Cherrytown
    "EF1_000": "-54951.887,41834.32,95000,95000",  # Rainbow Highland
    "ED1_000": "-73294.422, 102007.773, 145000, 145000",  # Droes Cave of Abyss
    "ED2_000": "-80964.461, 70370.664, 163000, 163000",  # Droes Under Valley

    "SR1_000": "-17627.172,29112.953,50000,50000",  # Ron
    "SR2_000": "-19470.254,28820.48,42000,42000",  # Kendal
    "SR3_000": "-22521.137,18068.002,34000,34000",  # Cony
    "AI1_000": "-22222.289, 33057.918, 50000, 50000",  # Clouds
    "AI2_000": "-22222.289, 33057.918, 50000, 50000",  # Aria
    "BI1_000": "-25574.053, 31762.715, 50000, 50000",  # Misty
    "BI3_000": "-23696.34, 26196.34, 50000, 50000",  # Gem
    "CI3_000": "-22222.289, 33057.918, 50000, 50000",  # Ease
    "CI5_000": "-22222.289, 33057.918, 50000, 50000",  # Eva
    "EI1_000": "-22222.289, 33057.918, 50000, 50000",  # Celestyn
    "EI4_000": "-22222.289, 33057.918, 50000, 50000",  # Selina

    "AS1_000": "-575773.875, 572256.063, 870000, 870000",  # Ocean
}


class Map(db.Model):
    __tablename__ = "map"

    _mapper_utils = {
        "files": {
            "string": [
                "AreaStr.dat"
            ],
        },
    }

    code = db.Column(db.String(32), primary_key=True, nullable=False)

    name = db.Column(db.String(128), nullable=False)

    left = CustomColumn(db.Float)
    top = CustomColumn(db.Float)
    width = CustomColumn(db.Float)
    height = CustomColumn(db.Float)

    map_points = db.relationship(
        "MapPoint", primaryjoin="foreign(MapPoint.map_code) == Map.code",
        viewonly=True,)

    def _parse_row(row: dict) -> "Map":
        code = row["Code"]
        lwth = MAP_CODE_TO_LTWH.get(code, None)

        if lwth is None:
            # Not a "real" map but rather island or an area
            # which only have a name and code
            return {
                "code": code,
                "name": row[LANGUAGE]
            }

        l, t, w, h = [float(num) for num in lwth.split(",")]

        return {
            "code": code,
            "name": row[LANGUAGE],
            "left": l,
            "top": t,
            "width": w,
            "height": h,
        }

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = {
            "code": self.code,
            "name": self.name,
            "left": self.left,
            "top": self.top,
            "width": self.width,
            "height": self.height,
        }

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "points": [point.to_dict(monster_dict=True)
                       for point in self.map_points]
        }
