from webapp.extensions import db


class Drop(db.Model):
    __tablename__ = "drop"

    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    monster_code = db.Column(db.String(32),
                             db.ForeignKey("monster.code"),
                             nullable=False)

    monster = db.relationship("Monster",
                              foreign_keys=[monster_code],
                              viewonly=True,)

    item_code = db.Column(db.String(32),
                          db.ForeignKey("item_list.code"),
                          nullable=False)

    item = db.relationship("ItemList",
                           foreign_keys=[item_code],
                           viewonly=True,)

    def to_dict(
        self,
        item_dict: bool = False,
        monster_dict: bool = False
    ) -> dict:
        if item_dict:
            return {
                "item": self.item.to_dict(with_item_data=True),
                "quantity": self.quantity,
            }

        elif monster_dict:
            return {
                "monster": self.monster.to_dict(minimal=True),
                "quantity": self.quantity,
            }
