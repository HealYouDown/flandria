from webapp.extensions import db
from webapp.models.custom_sql_classes import CustomColumn
from webapp.models.declarative_mixins import (DroppedByMixin, RandomBoxMixin,
                                              SoldByMixin)
from webapp.models.mixins import BaseMixin


class Recipe(
    db.Model, BaseMixin,
    DroppedByMixin, RandomBoxMixin, SoldByMixin,
):
    __tablename__ = "recipe"

    _mapper_utils = {
        "files": {
            "server": [
                "s_RecipeItem.bin"
            ],
            "client": [
                "c_RecipeItemRes.bin"
            ],
            "string": [
                "RecipeItemStr.dat"
            ]
        },
    }

    result_item_code = CustomColumn(
        db.String(32), db.ForeignKey("item_list.code"),
        nullable=False, mapper_key="결과물코드")

    result_item_quantity = CustomColumn(db.Integer, nullable=False,
                                        mapper_key="결과물수량")

    result_item = db.relationship("ItemList", foreign_keys=[result_item_code],
                                  viewonly=True,)

    # Material 1
    material_1_code = CustomColumn(
        db.String(32), db.ForeignKey("item_list.code"),
        mapper_key="재료1",
        transform=lambda v: v if v != "#" else None)

    material_1_quantity = CustomColumn(
        db.Integer, mapper_key="필요량1",
        transform=lambda v: v if v != 0 else None
    )

    material_1 = db.relationship("ItemList", foreign_keys=[material_1_code],
                                 viewonly=True,)

    # Material 2
    material_2_code = CustomColumn(
        db.String(32), db.ForeignKey("item_list.code"),
        mapper_key="재료2",
        transform=lambda v: v if v != "#" else None)

    material_2_quantity = CustomColumn(
        db.Integer, mapper_key="필요량2",
        transform=lambda v: v if v != 0 else None
    )

    material_2 = db.relationship("ItemList", foreign_keys=[material_2_code],
                                 viewonly=True,)

    # Material 3
    material_3_code = CustomColumn(
        db.String(32), db.ForeignKey("item_list.code"),
        mapper_key="재료3",
        transform=lambda v: v if v != "#" else None)

    material_3_quantity = CustomColumn(
        db.Integer, mapper_key="필요량3",
        transform=lambda v: v if v != 0 else None
    )

    material_3 = db.relationship("ItemList", foreign_keys=[material_3_code],
                                 viewonly=True,)

    # Material 4
    material_4_code = CustomColumn(
        db.String(32), db.ForeignKey("item_list.code"),
        mapper_key="재료4",
        transform=lambda v: v if v != "#" else None)

    material_4_quantity = CustomColumn(
        db.Integer, mapper_key="필요량4",
        transform=lambda v: v if v != 0 else None
    )

    material_4 = db.relationship("ItemList", foreign_keys=[material_4_code],
                                 viewonly=True,)

    # Material 5
    material_5_code = CustomColumn(
        db.String(32), db.ForeignKey("item_list.code"),
        mapper_key="재료5",
        transform=lambda v: v if v != "#" else None)

    material_5_quantity = CustomColumn(
        db.Integer, mapper_key="필요량5",
        transform=lambda v: v if v != 0 else None
    )

    material_5 = db.relationship("ItemList", foreign_keys=[material_5_code],
                                 viewonly=True,)

    # Material 6
    material_6_code = CustomColumn(
        db.String(32), db.ForeignKey("item_list.code"),
        mapper_key="재료6",
        transform=lambda v: v if v != "#" else None)

    material_6_quantity = CustomColumn(
        db.Integer, mapper_key="필요량6",
        transform=lambda v: v if v != 0 else None
    )

    material_6 = db.relationship("ItemList", foreign_keys=[material_6_code],
                                 viewonly=True,)

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = BaseMixin.to_dict(self, minimal)

        if minimal:
            return minimal_dict

        materials = []
        for i in range(1, 7):
            material_code = getattr(self, f"material_{i}_code")
            if material_code:
                materials.append({
                    "item": getattr(self, f"material_{i}").to_dict(),
                    "quantity": getattr(self, f"material_{i}_quantity"),
                })

        return {
            **minimal_dict,
            "result_item": self.result_item.to_dict(),
            "result_item_quantity": self.result_item_quantity,
            "materials": materials,
            **DroppedByMixin.to_dict(self),
            **SoldByMixin.to_dict(self),
            **RandomBoxMixin.to_dict(self),
        }
