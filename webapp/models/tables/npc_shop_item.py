from webapp.extensions import db


class NpcShopItem(db.Model):
    __tablename__ = "npc_shop_item"

    _mapper_utils = {
        "files": {
            "xml": [
                "StoreData.xml"
            ],
        },
    }

    index = db.Column(db.Integer, primary_key=True, autoincrement=True)

    npc_code = db.Column(db.String(32), db.ForeignKey("npc.code"),
                         nullable=False)
    npc = db.relationship("Npc", foreign_keys=[npc_code], viewonly=True,)

    npc_class = db.Column(db.Integer, nullable=False)  # idk what that is

    section_name = db.Column(db.String(64), nullable=False)
    section_type = db.Column(db.String(64), nullable=False)

    item_code = db.Column(db.String(32), db.ForeignKey("item_list.code"),
                          nullable=False)

    item = db.relationship("ItemList", foreign_keys=[item_code], viewonly=True)

    def to_dict(self, npc_dict: bool = False, item_dict: bool = False) -> dict:
        # npc dict is used to link from an item to the npc, while item dict
        # is used to link to the item from the npc.
        if npc_dict:
            return self.npc.to_dict()

        elif item_dict:
            return {
                "item": self.item.to_dict(with_item_data=True),
                "section_name": self.section_name,
                "section_type": self.section_type,
            }
