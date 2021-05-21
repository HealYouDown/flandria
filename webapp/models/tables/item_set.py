from webapp.extensions import db
from webapp.models.custom_sql_classes import CustomColumn
from webapp.models.enums import EffectCode
from webapp.models.transforms import bonus_value_transform, MAX_INT


class ItemSet(db.Model):
    __tablename__ = "item_set"

    _mapper_utils = {
        "files": {
            "server": [
                "s_SetItemData.bin"
            ],
            "string": [
                "SetNameStr.dat"
            ],
        },
    }

    code = CustomColumn(db.String(32), primary_key=True,
                        nullable=False, mapper_key="코드")

    name = CustomColumn(db.String(256), nullable=False,
                        mapper_key="_name")

    weapon_code = CustomColumn(
        db.String(32), db.ForeignKey("item_list.code"),
        mapper_key="무기",
        transform=lambda v: v if v != "#" else None)

    weapon = db.relationship("ItemList", foreign_keys=[weapon_code],
                             uselist=False, lazy="joined",
                             viewonly=True,)

    coat_code = CustomColumn(
        db.String(32), db.ForeignKey("item_list.code"),
        mapper_key="상의",
        transform=lambda v: v if v != "#" else None)

    coat = db.relationship("ItemList", foreign_keys=[coat_code],
                           uselist=False, lazy="joined",
                           viewonly=True,)

    pants_code = CustomColumn(
        db.String(32), db.ForeignKey("item_list.code"),
        mapper_key="하의",
        transform=lambda v: v if v != "#" else None)

    pants = db.relationship("ItemList", foreign_keys=[pants_code],
                            uselist=False, lazy="joined",
                            viewonly=True,)

    shoes_code = CustomColumn(
        db.String(32), db.ForeignKey("item_list.code"),
        mapper_key="신발",
        transform=lambda v: v if v != "#" else None)

    shoes = db.relationship("ItemList", foreign_keys=[shoes_code],
                            uselist=False, lazy="joined",
                            viewonly=True,)

    gauntlet_code = CustomColumn(
        db.String(32), db.ForeignKey("item_list.code"),
        mapper_key="장갑",
        transform=lambda v: v if v != "#" else None)

    gauntlet = db.relationship("ItemList", foreign_keys=[gauntlet_code],
                               uselist=False, lazy="joined",
                               viewonly=True,)

    shield_code = CustomColumn(
        db.String(32), db.ForeignKey("item_list.code"),
        mapper_key="방패",
        transform=lambda v: v if v != "#" else None)

    shield = db.relationship("ItemList", foreign_keys=[shield_code],
                             uselist=False, lazy="joined",
                             viewonly=True,)

    necklace_code = CustomColumn(
        db.String(32), db.ForeignKey("item_list.code"),
        mapper_key="목걸이",
        transform=lambda v: v if v != "#" else None)

    necklace = db.relationship("ItemList", foreign_keys=[necklace_code],
                               uselist=False, lazy="joined",
                               viewonly=True,)

    earring_code = CustomColumn(
        db.String(32), db.ForeignKey("item_list.code"),
        mapper_key="귀걸이",
        transform=lambda v: v if v != "#" else None)

    earring = db.relationship("ItemList", foreign_keys=[earring_code],
                              uselist=False, lazy="joined",
                              viewonly=True,)

    ring_1_code = CustomColumn(
        db.String(32), db.ForeignKey("item_list.code"),
        mapper_key="반지1",
        transform=lambda v: v if v != "#" else None)

    ring_1 = db.relationship("ItemList", foreign_keys=[ring_1_code],
                             uselist=False, lazy="joined",
                             viewonly=True,)

    ring_2_code = CustomColumn(
        db.String(32), db.ForeignKey("item_list.code"),
        mapper_key="반지2",
        transform=lambda v: v if v != "#" else None)

    ring_2 = db.relationship("ItemList", foreign_keys=[ring_2_code],
                             uselist=False, lazy="joined",
                             viewonly=True,)

    dress_code = CustomColumn(
        db.String(32), db.ForeignKey("item_list.code"),
        mapper_key="옷",
        transform=lambda v: v if v != "#" else None)

    dress = db.relationship("ItemList", foreign_keys=[dress_code],
                            uselist=False, lazy="joined",
                            viewonly=True,)

    hat_code = CustomColumn(
        db.String(32), db.ForeignKey("item_list.code"),
        mapper_key="모자",
        transform=lambda v: v if v != "#" else None)

    hat = db.relationship("ItemList", foreign_keys=[hat_code],
                          uselist=False, lazy="joined",
                          viewonly=True,)

    def to_dict(self) -> dict:
        item_columns = [self.weapon, self.coat, self.pants,
                        self.shoes, self.gauntlet, self.shield,
                        self.necklace, self.earring, self.ring_1,
                        self.ring_2, self.dress, self.hat]

        effects = []
        for i in range(1, 13):
            effect_code = getattr(self, f"effect_{i}_code")
            if effect_code:
                effects.append({
                    "code": effect_code.to_dict(),
                    "operator": getattr(self, f"effect_{i}_operator"),
                    "value": getattr(self, f"effect_{i}_value"),
                })

        return {
            "items": [item.to_dict(with_item_data=True)
                      for item in item_columns if item],
            "effects": effects,
        }


# Add effect columns
for i in range(1, 13):
    # Code
    setattr(ItemSet, f"effect_{i}_code",
            CustomColumn(db.Enum(EffectCode),
                         mapper_key=f"효과코드_{i}",
                         transform=(lambda v: EffectCode(v) if v != MAX_INT
                                    else None)))
    # Operator
    setattr(ItemSet, f"effect_{i}_operator",
            CustomColumn(
                db.String(4), mapper_key=f"수치연산자_{i}",
                transform=lambda v: v if v != "#" else None))

    # Value
    setattr(ItemSet, f"effect_{i}_value",
            CustomColumn(
                db.Float, mapper_key=f"효과값_{i}",
                transform=bonus_value_transform))
