from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from ...extensions import db
from .item_list import ItemList  # noqa F401
from ..mixins import BaseMixin


class RandomBox(db.Model, BaseMixin):
    __tablename__ = "random_box"
    __bind_key__ = "static_data"

    item_0_code = Column(String, ForeignKey("item_list.code"))
    item_0_quantity = Column(Integer)
    item_0_probability = Column(Float)
    item_0 = relationship("ItemList",
                          foreign_keys=[item_0_code],
                          lazy="joined")

    item_1_code = Column(String, ForeignKey("item_list.code"))
    item_1_quantity = Column(Integer)
    item_1_probability = Column(Float)
    item_1 = relationship("ItemList",
                          foreign_keys=[item_1_code],
                          lazy="joined")

    item_2_code = Column(String, ForeignKey("item_list.code"))
    item_2_quantity = Column(Integer)
    item_2_probability = Column(Float)
    item_2 = relationship("ItemList",
                          foreign_keys=[item_2_code],
                          lazy="joined")

    item_3_code = Column(String, ForeignKey("item_list.code"))
    item_3_quantity = Column(Integer)
    item_3_probability = Column(Float)
    item_3 = relationship("ItemList",
                          foreign_keys=[item_3_code],
                          lazy="joined")

    item_4_code = Column(String, ForeignKey("item_list.code"))
    item_4_quantity = Column(Integer)
    item_4_probability = Column(Float)
    item_4 = relationship("ItemList",
                          foreign_keys=[item_4_code],
                          lazy="joined")

    item_5_code = Column(String, ForeignKey("item_list.code"))
    item_5_quantity = Column(Integer)
    item_5_probability = Column(Float)
    item_5 = relationship("ItemList",
                          foreign_keys=[item_5_code],
                          lazy="joined")

    item_6_code = Column(String, ForeignKey("item_list.code"))
    item_6_quantity = Column(Integer)
    item_6_probability = Column(Float)
    item_6 = relationship("ItemList",
                          foreign_keys=[item_6_code],
                          lazy="joined")

    item_7_code = Column(String, ForeignKey("item_list.code"))
    item_7_quantity = Column(Integer)
    item_7_probability = Column(Float)
    item_7 = relationship("ItemList",
                          foreign_keys=[item_7_code],
                          lazy="joined")

    item_8_code = Column(String, ForeignKey("item_list.code"))
    item_8_quantity = Column(Integer)
    item_8_probability = Column(Float)
    item_8 = relationship("ItemList",
                          foreign_keys=[item_8_code],
                          lazy="joined")

    item_9_code = Column(String, ForeignKey("item_list.code"))
    item_9_quantity = Column(Integer)
    item_9_probability = Column(Float)
    item_9 = relationship("ItemList",
                          foreign_keys=[item_9_code],
                          lazy="joined")

    item_10_code = Column(String, ForeignKey("item_list.code"))
    item_10_quantity = Column(Integer)
    item_10_probability = Column(Float)
    item_10 = relationship("ItemList",
                           foreign_keys=[item_10_code],
                           lazy="joined")

    item_11_code = Column(String, ForeignKey("item_list.code"))
    item_11_quantity = Column(Integer)
    item_11_probability = Column(Float)
    item_11 = relationship("ItemList",
                           foreign_keys=[item_11_code],
                           lazy="joined")

    item_12_code = Column(String, ForeignKey("item_list.code"))
    item_12_quantity = Column(Integer)
    item_12_probability = Column(Float)
    item_12 = relationship("ItemList",
                           foreign_keys=[item_12_code],
                           lazy="joined")

    item_13_code = Column(String, ForeignKey("item_list.code"))
    item_13_quantity = Column(Integer)
    item_13_probability = Column(Float)
    item_13 = relationship("ItemList",
                           foreign_keys=[item_13_code],
                           lazy="joined")

    item_14_code = Column(String, ForeignKey("item_list.code"))
    item_14_quantity = Column(Integer)
    item_14_probability = Column(Float)
    item_14 = relationship("ItemList",
                           foreign_keys=[item_14_code],
                           lazy="joined")

    item_15_code = Column(String, ForeignKey("item_list.code"))
    item_15_quantity = Column(Integer)
    item_15_probability = Column(Float)
    item_15 = relationship("ItemList",
                           foreign_keys=[item_15_code],
                           lazy="joined")

    item_16_code = Column(String, ForeignKey("item_list.code"))
    item_16_quantity = Column(Integer)
    item_16_probability = Column(Float)
    item_16 = relationship("ItemList",
                           foreign_keys=[item_16_code],
                           lazy="joined")

    item_17_code = Column(String, ForeignKey("item_list.code"))
    item_17_quantity = Column(Integer)
    item_17_probability = Column(Float)
    item_17 = relationship("ItemList",
                           foreign_keys=[item_17_code],
                           lazy="joined")

    item_18_code = Column(String, ForeignKey("item_list.code"))
    item_18_quantity = Column(Integer)
    item_18_probability = Column(Float)
    item_18 = relationship("ItemList",
                           foreign_keys=[item_18_code],
                           lazy="joined")

    item_19_code = Column(String, ForeignKey("item_list.code"))
    item_19_quantity = Column(Integer)
    item_19_probability = Column(Float)
    item_19 = relationship("ItemList",
                           foreign_keys=[item_19_code],
                           lazy="joined")

    item_20_code = Column(String, ForeignKey("item_list.code"))
    item_20_quantity = Column(Integer)
    item_20_probability = Column(Float)
    item_20 = relationship("ItemList",
                           foreign_keys=[item_20_code],
                           lazy="joined")

    item_21_code = Column(String, ForeignKey("item_list.code"))
    item_21_quantity = Column(Integer)
    item_21_probability = Column(Float)
    item_21 = relationship("ItemList",
                           foreign_keys=[item_21_code],
                           lazy="joined")

    item_22_code = Column(String, ForeignKey("item_list.code"))
    item_22_quantity = Column(Integer)
    item_22_probability = Column(Float)
    item_22 = relationship("ItemList",
                           foreign_keys=[item_22_code],
                           lazy="joined")

    item_23_code = Column(String, ForeignKey("item_list.code"))
    item_23_quantity = Column(Integer)
    item_23_probability = Column(Float)
    item_23 = relationship("ItemList",
                           foreign_keys=[item_23_code],
                           lazy="joined")

    item_24_code = Column(String, ForeignKey("item_list.code"))
    item_24_quantity = Column(Integer)
    item_24_probability = Column(Float)
    item_24 = relationship("ItemList",
                           foreign_keys=[item_24_code],
                           lazy="joined")

    item_25_code = Column(String, ForeignKey("item_list.code"))
    item_25_quantity = Column(Integer)
    item_25_probability = Column(Float)
    item_25 = relationship("ItemList",
                           foreign_keys=[item_25_code],
                           lazy="joined")

    item_26_code = Column(String, ForeignKey("item_list.code"))
    item_26_quantity = Column(Integer)
    item_26_probability = Column(Float)
    item_26 = relationship("ItemList",
                           foreign_keys=[item_26_code],
                           lazy="joined")

    item_27_code = Column(String, ForeignKey("item_list.code"))
    item_27_quantity = Column(Integer)
    item_27_probability = Column(Float)
    item_27 = relationship("ItemList",
                           foreign_keys=[item_27_code],
                           lazy="joined")

    item_28_code = Column(String, ForeignKey("item_list.code"))
    item_28_quantity = Column(Integer)
    item_28_probability = Column(Float)
    item_28 = relationship("ItemList",
                           foreign_keys=[item_28_code],
                           lazy="joined")

    item_29_code = Column(String, ForeignKey("item_list.code"))
    item_29_quantity = Column(Integer)
    item_29_probability = Column(Float)
    item_29 = relationship("ItemList",
                           foreign_keys=[item_29_code],
                           lazy="joined")

    item_30_code = Column(String, ForeignKey("item_list.code"))
    item_30_quantity = Column(Integer)
    item_30_probability = Column(Float)
    item_30 = relationship("ItemList",
                           foreign_keys=[item_30_code],
                           lazy="joined")

    item_31_code = Column(String, ForeignKey("item_list.code"))
    item_31_quantity = Column(Integer)
    item_31_probability = Column(Float)
    item_31 = relationship("ItemList",
                           foreign_keys=[item_31_code],
                           lazy="joined")

    item_32_code = Column(String, ForeignKey("item_list.code"))
    item_32_quantity = Column(Integer)
    item_32_probability = Column(Float)
    item_32 = relationship("ItemList",
                           foreign_keys=[item_32_code],
                           lazy="joined")

    item_33_code = Column(String, ForeignKey("item_list.code"))
    item_33_quantity = Column(Integer)
    item_33_probability = Column(Float)
    item_33 = relationship("ItemList",
                           foreign_keys=[item_33_code],
                           lazy="joined")

    item_34_code = Column(String, ForeignKey("item_list.code"))
    item_34_quantity = Column(Integer)
    item_34_probability = Column(Float)
    item_34 = relationship("ItemList",
                           foreign_keys=[item_34_code],
                           lazy="joined")

    item_35_code = Column(String, ForeignKey("item_list.code"))
    item_35_quantity = Column(Integer)
    item_35_probability = Column(Float)
    item_35 = relationship("ItemList",
                           foreign_keys=[item_35_code],
                           lazy="joined")

    item_36_code = Column(String, ForeignKey("item_list.code"))
    item_36_quantity = Column(Integer)
    item_36_probability = Column(Float)
    item_36 = relationship("ItemList",
                           foreign_keys=[item_36_code],
                           lazy="joined")

    item_37_code = Column(String, ForeignKey("item_list.code"))
    item_37_quantity = Column(Integer)
    item_37_probability = Column(Float)
    item_37 = relationship("ItemList",
                           foreign_keys=[item_37_code],
                           lazy="joined")

    item_38_code = Column(String, ForeignKey("item_list.code"))
    item_38_quantity = Column(Integer)
    item_38_probability = Column(Float)
    item_38 = relationship("ItemList",
                           foreign_keys=[item_38_code],
                           lazy="joined")

    item_39_code = Column(String, ForeignKey("item_list.code"))
    item_39_quantity = Column(Integer)
    item_39_probability = Column(Float)
    item_39 = relationship("ItemList",
                           foreign_keys=[item_39_code],
                           lazy="joined")

    item_40_code = Column(String, ForeignKey("item_list.code"))
    item_40_quantity = Column(Integer)
    item_40_probability = Column(Float)
    item_40 = relationship("ItemList",
                           foreign_keys=[item_40_code],
                           lazy="joined")

    item_41_code = Column(String, ForeignKey("item_list.code"))
    item_41_quantity = Column(Integer)
    item_41_probability = Column(Float)
    item_41 = relationship("ItemList",
                           foreign_keys=[item_41_code],
                           lazy="joined")

    item_42_code = Column(String, ForeignKey("item_list.code"))
    item_42_quantity = Column(Integer)
    item_42_probability = Column(Float)
    item_42 = relationship("ItemList",
                           foreign_keys=[item_42_code],
                           lazy="joined")

    item_43_code = Column(String, ForeignKey("item_list.code"))
    item_43_quantity = Column(Integer)
    item_43_probability = Column(Float)
    item_43 = relationship("ItemList",
                           foreign_keys=[item_43_code],
                           lazy="joined")

    item_44_code = Column(String, ForeignKey("item_list.code"))
    item_44_quantity = Column(Integer)
    item_44_probability = Column(Float)
    item_44 = relationship("ItemList",
                           foreign_keys=[item_44_code],
                           lazy="joined")

    item_45_code = Column(String, ForeignKey("item_list.code"))
    item_45_quantity = Column(Integer)
    item_45_probability = Column(Float)
    item_45 = relationship("ItemList",
                           foreign_keys=[item_45_code],
                           lazy="joined")

    item_46_code = Column(String, ForeignKey("item_list.code"))
    item_46_quantity = Column(Integer)
    item_46_probability = Column(Float)
    item_46 = relationship("ItemList",
                           foreign_keys=[item_46_code],
                           lazy="joined")

    item_47_code = Column(String, ForeignKey("item_list.code"))
    item_47_quantity = Column(Integer)
    item_47_probability = Column(Float)
    item_47 = relationship("ItemList",
                           foreign_keys=[item_47_code],
                           lazy="joined")

    item_48_code = Column(String, ForeignKey("item_list.code"))
    item_48_quantity = Column(Integer)
    item_48_probability = Column(Float)
    item_48 = relationship("ItemList",
                           foreign_keys=[item_48_code],
                           lazy="joined")

    item_49_code = Column(String, ForeignKey("item_list.code"))
    item_49_quantity = Column(Integer)
    item_49_probability = Column(Float)
    item_49 = relationship("ItemList",
                           foreign_keys=[item_49_code],
                           lazy="joined")

    item_50_code = Column(String, ForeignKey("item_list.code"))
    item_50_quantity = Column(Integer)
    item_50_probability = Column(Float)
    item_50 = relationship("ItemList",
                           foreign_keys=[item_50_code],
                           lazy="joined")

    item_51_code = Column(String, ForeignKey("item_list.code"))
    item_51_quantity = Column(Integer)
    item_51_probability = Column(Float)
    item_51 = relationship("ItemList",
                           foreign_keys=[item_51_code],
                           lazy="joined")

    item_52_code = Column(String, ForeignKey("item_list.code"))
    item_52_quantity = Column(Integer)
    item_52_probability = Column(Float)
    item_52 = relationship("ItemList",
                           foreign_keys=[item_52_code],
                           lazy="joined")

    item_53_code = Column(String, ForeignKey("item_list.code"))
    item_53_quantity = Column(Integer)
    item_53_probability = Column(Float)
    item_53 = relationship("ItemList",
                           foreign_keys=[item_53_code],
                           lazy="joined")

    item_54_code = Column(String, ForeignKey("item_list.code"))
    item_54_quantity = Column(Integer)
    item_54_probability = Column(Float)
    item_54 = relationship("ItemList",
                           foreign_keys=[item_54_code],
                           lazy="joined")

    item_55_code = Column(String, ForeignKey("item_list.code"))
    item_55_quantity = Column(Integer)
    item_55_probability = Column(Float)
    item_55 = relationship("ItemList",
                           foreign_keys=[item_55_code],
                           lazy="joined")

    item_56_code = Column(String, ForeignKey("item_list.code"))
    item_56_quantity = Column(Integer)
    item_56_probability = Column(Float)
    item_56 = relationship("ItemList",
                           foreign_keys=[item_56_code],
                           lazy="joined")

    item_57_code = Column(String, ForeignKey("item_list.code"))
    item_57_quantity = Column(Integer)
    item_57_probability = Column(Float)
    item_57 = relationship("ItemList",
                           foreign_keys=[item_57_code],
                           lazy="joined")

    item_58_code = Column(String, ForeignKey("item_list.code"))
    item_58_quantity = Column(Integer)
    item_58_probability = Column(Float)
    item_58 = relationship("ItemList",
                           foreign_keys=[item_58_code],
                           lazy="joined")

    item_59_code = Column(String, ForeignKey("item_list.code"))
    item_59_quantity = Column(Integer)
    item_59_probability = Column(Float)
    item_59 = relationship("ItemList",
                           foreign_keys=[item_59_code],
                           lazy="joined")

    item_60_code = Column(String, ForeignKey("item_list.code"))
    item_60_quantity = Column(Integer)
    item_60_probability = Column(Float)
    item_60 = relationship("ItemList",
                           foreign_keys=[item_60_code],
                           lazy="joined")

    def to_dict(
        self,
        minimal: bool = False,
        can_see_probability: bool = False
    ) -> dict:
        minimal_dict = BaseMixin.to_dict(self, minimal)

        if minimal:
            return minimal_dict

        content = []
        for i in range(0, 61):
            item_code = getattr(self, f"item_{i}_code")
            if item_code != "#":
                item = getattr(self, f"item_{i}")
                probability = getattr(self, f"item_{i}_probability")
                quantity = getattr(self, f"item_{i}_quantity")

                if item_code == "money":
                    d = {
                        "quantity": quantity,
                        "item": {
                            "code": "money",
                            "name": "Gelt",
                            "icon": "def004.png",
                        }
                    }
                else:
                    d = {
                        "quantity": quantity,
                        "item": item.to_dict()
                    }
                if can_see_probability:
                    d["probability"] = probability,

                content.append(d)

                continue
            break

        return {
            **minimal_dict,
            "content": content
        }
