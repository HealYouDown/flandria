from typing import TYPE_CHECKING, cast

from src.updater.file_data import FileData
from src.updater.helpers import map_row_to_model
from src.updater.transforms import probability_to_float

if TYPE_CHECKING:
    from src.database.types import ModelCls
    from src.updater.schema import LoaderInfo

    from .types import T_STRATEGY_RETURN

# Unused from previous essence concept
EXCLUDE_CODES = [
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


def random_box(
    model_cls: "ModelCls",
    loader_info: "LoaderInfo",
) -> "T_STRATEGY_RETURN":
    from src.database.models import RandomBoxReward

    data = FileData.from_files(loader_info.files)

    boxes: list[dict] = []
    rewards: list[dict] = []
    for row in data.server_data:
        pk, obj = map_row_to_model(model_cls, row, data)
        if cast(str, pk) in EXCLUDE_CODES:
            continue

        for i in range(0, 61):
            reward_code = row[f"보상{i}"]
            quantity = row[f"보상수량{i}"]
            probability = probability_to_float(cast(int, row[f"보상확률{i}"]))

            # We don't break if there is no reward code, because AHA
            # might have skipped a key (yep, idk)
            if reward_code is not None:
                rewards.append(
                    {
                        "random_box_code": pk,
                        "reward_code": reward_code,
                        "quantity": quantity,
                        "probability": probability,
                    }
                )

        boxes.append(obj)

    return [
        (model_cls, boxes),
        (RandomBoxReward, rewards),
    ]
