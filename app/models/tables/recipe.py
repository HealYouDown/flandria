from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ...extensions import db
from ..mixins import BaseMixin


class Recipe(db.Model, BaseMixin):
    __tablename__ = "recipe"
    __bind_key__ = "static_data"

    result_code = Column(String, ForeignKey("item_list.code"))
    result_quantity = Column(Integer)
    result_item = relationship("ItemList", foreign_keys=[result_code])

    material_1_code = Column(String, ForeignKey("item_list.code"))
    material_1_quantity = Column(Integer)
    material_1 = relationship("ItemList", foreign_keys=[material_1_code])

    material_2_code = Column(String, ForeignKey("item_list.code"))
    material_2_quantity = Column(Integer)
    material_2 = relationship("ItemList", foreign_keys=[material_2_code])

    material_3_code = Column(String, ForeignKey("item_list.code"))
    material_3_quantity = Column(Integer)
    material_3 = relationship("ItemList", foreign_keys=[material_3_code])

    material_4_code = Column(String, ForeignKey("item_list.code"))
    material_4_quantity = Column(Integer)
    material_4 = relationship("ItemList", foreign_keys=[material_4_code])

    material_5_code = Column(String, ForeignKey("item_list.code"))
    material_5_quantity = Column(Integer)
    material_5 = relationship("ItemList", foreign_keys=[material_5_code])

    material_6_code = Column(String, ForeignKey("item_list.code"))
    material_6_quantity = Column(Integer)
    material_6 = relationship("ItemList", foreign_keys=[material_6_code])

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = BaseMixin.to_dict(self, minimal)

        if minimal:
            return minimal_dict

        materials = []
        for i in range(1, 7):
            quantity = getattr(self, f"material_{i}_quantity")
            item = getattr(self, f"material_{i}")
            if item is not None:
                item_dict = item.to_dict()
                materials.append({
                    "quantity": quantity,
                    "item": item_dict
                })
                continue
            break

        return {
            **minimal_dict,
            "result_quantity": self.result_quantity,
            "result_item": self.result_item.to_dict(),
            "materials": materials
        }
