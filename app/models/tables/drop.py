from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ...extensions import db


class Drop(db.Model):
    __tablename__ = "drop"
    __bind_key__ = "unstatic_data"

    index = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer, default=1, nullable=False)

    monster_code = Column(String,
                          ForeignKey("monster.code"),
                          nullable=False)
    monster = relationship("Monster",
                           foreign_keys=[monster_code],)

    item_code = Column(String,
                       ForeignKey("item_list.code"),
                       nullable=False)
    item = relationship("ItemList",
                        foreign_keys=[item_code],
                        )

    def to_dict(self,
                exclude_monster: bool = False,
                exclude_item: bool = False
                ) -> dict:
        d = {
            "id": self.index,
        }

        if not exclude_monster:
            d["monster"] = self.monster.to_dict(minimal=True)

        if not exclude_item:
            d["quantity"] = self.quantity
            d["item"] = self.item.to_dict()

        return d
