from webapp.extensions import db
from webapp.models.custom_sql_classes import CustomColumn
from webapp.models.declarative_mixins import (DroppedByMixin, NeededForMixin,
                                              ProducedByMixin, RandomBoxMixin,
                                              SoldByMixin)
from webapp.models.mixins import BaseMixin
from webapp.models.transforms import MAX_INT, florensia_probability_transform

EXCLUDES = [
    "rbvip0000",
    "rbessc001",
    "rbessc002",
    "rbessc003",
    "rbessc004",
    "rbessc005",
    "rbessc006",
    "rbessc007",
    "rbessc008",
    "rbessc009",
    "rbessc010",
    "rbessc011",
    "rbessc012",
    "rbessc013",
    "rbessc014",
    "rbessc015",
    "rbessc016",
    "rbessc017",
    "rbessc018",
    "rbessc019",
    "rbessc020",
    "rbessc021",
    "rbessc022",
    "rbessc023",
    "rbessc024",
    "rbessc025",
    "rbessc026",
    "rbessc027",
    "rbessc028",
    "rbessc029",
    "rbessc030",
    "rbessc031",
    "rbessc032",
    "rbessc033",
    "rbessc034",
    "rbessc035",
    "rbessc036",
    "rbessc037",
    "rbessc038",
    "rbessc039",
    "rbessc040",
    "rbessc041",
    "rbessc042",
    "rbessc043",
    "rbessc044",
    "rbessc045",
    "rbessc046",
    "rbessc047",
    "rbessc048",
    "rbessc049",
    "rbessc050",
    "rbessc051",
    "rbessc052",
    "rbessc053",
    "rbessc054",
    "rbessc055",
    "rbessc056",
    "rbessc057",
    "rbessc058",
    "rbessc059",
    "rbessc060",
    "rbessc061",
    "rbessc062",
    "rbessc063",
    "rbessc064",
    "rbessc065",
    "rbessc066",
    "rbessc067",
    "rbessc068",
    "rbessc069",
    "rbessc070",
    "rbessc071",
    "rbessc072",
    "rbessc073",
    "rbessc074",
    "rbessc075",
    "rbessc076",
    "rbessc077",
    "rbessc078",
    "rbessc079",
    "rbessc080",
    "rbessc081",
    "rbessc082",
    "rbessc083",
    "rbessc084",
    "rbessc085",
    "rbessc086",
    "rbessc087",
    "rbessc088",
    "rbessc089",
    "rbessc090",
    "rbessc091",
    "rbessc092",
    "rbessc093",
    "rbessc094",
    "rbessc095",
    "rbessc096",
    "rbessc097",
    "rbessc098",
    "rbessc099",
    "rbessc100",
    "rbessc101",
    "rbessc102",
    "rbessc103",
    "rbessc104",
    "rbessc105",
    "rbessc106",
    "rbessc107",
    "rbessc108",
    "rbessc109",
    "rbessc110",
    "rbessc111",
    "rbessc112",
    "rbessc113",
    "rbessc114",
    "rbessc115",
    "rbessc116",
    "rbessc117",
    "rbessc118",
    "rbessc119",
    "rbessc120",
    "rbessc121",
    "rbessc122",
    "rbessc123",
    "rbessc124",
    "rbessc125",
    "rbessc126",
    "rbessc127",
    "rbessc128",
    "rbessc129",
    "rbessc130",
    "rbessc131",
    "rbessc132",
    "rbessc133",
    "rbessc134",
    "rbessc135",
    "rbessc136",
    "rbessc137",
    "rbessc138",
    "rbessc139",
    "rbessc140",
]


class RandomBox(
    db.Model, BaseMixin,
    DroppedByMixin, ProducedByMixin, NeededForMixin, SoldByMixin,
    RandomBoxMixin,
):
    __tablename__ = "random_box"

    _mapper_utils = {
        "files": {
            "server": [
                "s_RandomBoxItem.bin"
            ],
            "client": [
                "c_RandomBoxItemRes.bin"
            ],
            "string": [
                "RandomBoxItemStr.dat"
            ],
        },
        "filter": lambda row: row["코드"] not in EXCLUDES,
    }

    level_land = CustomColumn(db.Integer, nullable=False,
                              mapper_key="육상LV",
                              transform=lambda v: v if v != MAX_INT else 1)

    level_sea = CustomColumn(db.Integer, nullable=False,
                             mapper_key="해상LV",
                             transform=lambda v: v if v != MAX_INT else 1)

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = {
            **BaseMixin.to_dict(self, minimal),
            "level_land": self.level_land,
            "level_sea": self.level_sea,
        }

        if minimal:
            return minimal_dict

        items = []
        for i in range(0, 62):
            item_code = getattr(self, f"item_{i}_code")
            if item_code:
                if item_code == "money":
                    item = {
                        "code": "money",
                        "name": "Gelt",
                        "icon": "def004.png",
                        "rare_grade": 0,
                        "table": None,
                    }
                else:
                    item = getattr(self, f"item_{i}").to_dict()

                items.append({
                    "item": item,
                    "quantity": getattr(self, f"item_{i}_quantity"),
                })

        return {
            **minimal_dict,
            "items": items,
            **NeededForMixin.to_dict(self),
            **ProducedByMixin.to_dict(self),
            **DroppedByMixin.to_dict(self),
            **SoldByMixin.to_dict(self),
            **RandomBoxMixin.to_dict(self),
        }


# 0 - 60 = 61 items per box
for i in range(0, 62):
    # Code
    setattr(RandomBox, f"item_{i}_code",
            CustomColumn(
                db.String(32), db.ForeignKey("item_list.code"),
                mapper_key=f"보상{i}",
                transform=lambda v: v if v != "#" else None))

    # Quantity
    setattr(RandomBox, f"item_{i}_quantity",
            CustomColumn(
                    db.Integer, mapper_key=f"보상수량{i}",
                    transform=lambda v: v if v != 0 else None
                ))

    # Chance
    setattr(RandomBox, f"item_{i}_chance",
            CustomColumn(
                db.Float, mapper_key=f"보상확률{i}",
                transform=(
                    lambda v: florensia_probability_transform(v) if v != 0
                    else None)))

    # Relationship
    setattr(RandomBox, f"item_{i}",
            db.relationship(
                "ItemList",
                foreign_keys=[getattr(RandomBox, f"item_{i}_code")],
                viewonly=True)
            )
