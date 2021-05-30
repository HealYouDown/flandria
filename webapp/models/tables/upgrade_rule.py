
from database_updater.conversions import convert_integer
from webapp.extensions import db
from webapp.models.custom_sql_classes import CustomColumn
from webapp.models.transforms import MAX_INT


class UpgradeRule(db.Model):
    __tablename__ = "upgrade_rule"

    _mapper_utils = {
        "files": {
            "server": [
                "s_UpgradeRule.bin"
            ],
        },
    }

    index = db.Column(db.Integer, primary_key=True, autoincrement=True)

    code = CustomColumn(
        db.String(32), nullable=False,
        mapper_key="코드",
        # Replaces the last two numbers of each code
        # to 00 to allow for easier querying.
        # e.g. ruoh0107 -> ruoh0100
        transform=lambda v: v[:-2] + "00")

    upgrade_level = CustomColumn(db.Integer, nullable=False,
                                 mapper_key="업그레이드레벨")

    upgrade_cost = CustomColumn(db.Integer, nullable=False,
                                mapper_key="강화소모gelt")

    # Effect 0
    effect_0_code = CustomColumn(
        db.Integer, mapper_key="효과코드0",
        transform=lambda v: v if v != MAX_INT else None)

    effect_0_operator = CustomColumn(db.String(4), mapper_key="연산자0")

    effect_0_value = CustomColumn(
        db.Float, mapper_key="효과값0",
        transform=lambda v: convert_integer(v) if v != MAX_INT else None)

    # Effect 1
    effect_1_code = CustomColumn(
        db.Integer, mapper_key="효과코드1",
        transform=lambda v: v if v != MAX_INT else None)

    effect_1_operator = CustomColumn(db.String(4), mapper_key="연산자1")

    effect_1_value = CustomColumn(
        db.Float, mapper_key="효과값1",
        transform=lambda v: convert_integer(v) if v != MAX_INT else None)

    # Effect 2
    effect_2_code = CustomColumn(
        db.Integer, mapper_key="효과코드2",
        transform=lambda v: v if v != MAX_INT else None)

    effect_2_operator = CustomColumn(db.String(4), mapper_key="연산자2")

    effect_2_value = CustomColumn(
        db.Float, mapper_key="효과값2",
        transform=lambda v: convert_integer(v) if v != MAX_INT else None)

    # Effect 3
    effect_3_code = CustomColumn(
        db.Integer, mapper_key="효과코드3",
        transform=lambda v: v if v != MAX_INT else None)

    effect_3_operator = CustomColumn(db.String(4), mapper_key="연산자3")

    effect_3_value = CustomColumn(
        db.Float, mapper_key="효과값3",
        transform=lambda v: convert_integer(v) if v != MAX_INT else None)

    def to_dict(self) -> dict:
        # Here, effects are not grouped in a list as
        # they have to be referenced by the number later.
        effects = {}
        for i in range(0, 4):
            effects[f"effect_{i}"] = {
                "code": getattr(self, f"effect_{i}_code"),
                "operator": getattr(self, f"effect_{i}_operator"),
                "value": getattr(self, f"effect_{i}_value"),
            }

        return {
            "code": self.code,
            "upgrade_level": self.upgrade_level,
            "upgrade_cost": self.upgrade_cost,
            "effects": effects,
        }
