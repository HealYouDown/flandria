from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import db


class NPCShop(db.Model):
    __tablename__ = "npc_shop"
    index = Column(Integer, primary_key=True, autoincrement=True)

    npc_code = Column(String, ForeignKey("npc.code"))
    npc = relationship("NPC", foreign_keys=[npc_code])

    item_code = Column(String, ForeignKey("item_list.code"))
    item = relationship("ItemList", foreign_keys=[item_code])

    def to_dict(self, minimal: bool = False) -> dict:
        return {
            "npc": self.npc.to_dict(),
            "item": self.item.to_dict(minimal=True)
        }
