from webapp.extensions import db
from webapp.models.custom_sql_classes import CustomColumn


class Npc(db.Model):
    __tablename__ = "npc"

    _mapper_utils = {
        "files": {
            "server": [
                "s_MerchantChar.bin",
                "s_GuardChar.bin",
                "s_CitizenChar.bin"
            ],
            "client": [
                "c_MerchantCharRes.bin",
                "c_GuardCharRes.bin",
                "c_CitizenCharRes.bin"
            ],
            "string": [
                "MerchantCharStr.dat",
                "GuardCharStr.dat",
                "CitizenCharStr.dat"
            ],
        },
        "options": {
            "image_key": "모델명"
        }
    }

    index = db.Column(db.Integer, nullable=False)

    code = CustomColumn(db.String(32), primary_key=True, nullable=False,
                        mapper_key="코드")

    name = CustomColumn(db.String(128), nullable=False,
                        mapper_key="_name",
                        index=True)

    icon = CustomColumn(db.String(128), nullable=False,
                        mapper_key="_icon")

    level = CustomColumn(db.Integer, nullable=False,
                         mapper_key="기준레벨")

    shop_items = db.relationship(
        "NpcShopItem",
        primaryjoin="foreign(NpcShopItem.npc_code) == Npc.code",
        viewonly=True,
    )

    quests = db.relationship(
        "Quest",
        primaryjoin="foreign(Quest.start_npc_code) == Npc.code",
        viewonly=True,
    )

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = {
            "code": self.code,
            "name": self.name,
            "icon": self.icon,
            "level": self.level,
        }

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "shop_items": [shop_item.to_dict(item_dict=True)
                           for shop_item in self.shop_items
                           # Some NPCs sell items that do no longer exist
                           # or are not included in the database (like
                           # commerce goods), so those will be filtered
                           # out for now to prevent errors.
                           if shop_item.item],
            "quests": [quest.to_dict(minimal=True) for quest in self.quests],
        }
