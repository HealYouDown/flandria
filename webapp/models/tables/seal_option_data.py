from webapp.extensions import db
from webapp.models.custom_sql_classes import CustomColumn
from webapp.models.enums import EffectCode
from webapp.models.transforms import convert_integer


class SealOptionData(db.Model):
    __tablename__ = "seal_option_data"

    _mapper_utils = {
        "files": {
            "server": [
                "s_SealOptionValueData.bin"
            ]
        },
    }

    code = CustomColumn(db.String(32), primary_key=True,
                        mapper_key="코드")

    effect_code = CustomColumn(db.Enum(EffectCode), nullable=False,
                               mapper_key="효과코드",
                               transform=lambda v: EffectCode(v))

    operator = CustomColumn(db.String(4), mapper_key="Operator",
                            transform=lambda v: v if v != "#" else None)

    def to_dict(self) -> dict:
        intervalls = {}
        for cname in COLUMN_NAMES:
            intervalls[cname.lower()] = getattr(self, cname)

        return {
            "code": self.code,
            "effect_code": self.effect_code.to_dict(),
            "operator": self.operator,
            "intervalls": intervalls,
        }


# Dynamically add all those columns to the model
COLUMN_NAMES = [
    "Interval0101", "Interval0102", "Interval0103", "Interval0104",
    "Interval0105", "Interval0201", "Interval0202", "Interval0203",
    "Interval0204", "Interval0205", "Interval0301", "Interval0302",
    "Interval0303", "Interval0304", "Interval0305", "Interval0401",
    "Interval0402", "Interval0403", "Interval0404", "Interval0405",
    "Interval0501", "Interval0502", "Interval0503", "Interval0504",
    "Interval0505", "Interval0601", "Interval0602", "Interval0603",
    "Interval0604", "Interval0605", "Interval0701", "Interval0702",
    "Interval0703", "Interval0704", "Interval0705", "Interval0801",
    "Interval0802", "Interval0803", "Interval0804", "Interval0805",
    "Interval0901", "Interval0902", "Interval0903", "Interval0904",
    "Interval0905", "Interval1001", "Interval1002", "Interval1003",
    "Interval1004", "Interval1005", "Interval1101", "Interval1102",
    "Interval1103", "Interval1104", "Interval1105"
]

for column_name in COLUMN_NAMES:
    setattr(
        SealOptionData,
        column_name.lower(),
        CustomColumn(
            db.Float, mapper_key=column_name,
            transform=lambda v: convert_integer(v) if v != 0 else None))
