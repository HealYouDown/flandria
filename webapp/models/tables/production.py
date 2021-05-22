from webapp.extensions import db
from webapp.models.custom_sql_classes import CustomColumn
from webapp.models.enums import ProductionType


class Production(db.Model):
    __tablename__ = "production"

    _mapper_utils = {
        "files": {
            "server": [
                "s_Production.bin"
            ]
        },
    }

    index = db.Column(db.Integer, nullable=False)

    code = CustomColumn(db.String(32), primary_key=True,
                        mapper_key="코드")

    production_type = CustomColumn(
        db.Enum(ProductionType), nullable=False,
        mapper_key="타입", transform=lambda v: ProductionType(v))

    points_needed = CustomColumn(db.Integer, nullable=False,
                                 mapper_key="필요숙련도")

    division = CustomColumn(db.Integer, nullable=False,
                            mapper_key="구분")

    result_item_code = CustomColumn(
        db.String(32), db.ForeignKey("item_list.code"),
        nullable=False, mapper_key="결과물코드")

    result_item_quantity = CustomColumn(db.Integer, nullable=False,
                                        mapper_key="결과물수량")

    result_item = db.relationship("ItemList", foreign_keys=[result_item_code],
                                  lazy="joined", viewonly=True,)

    is_premium_essence = CustomColumn(db.Boolean, nullable=False,
                                      mapper_key="_premium_essence",)

    # FIXME: This includes the same production that is the parent as well
    # somehow foreign(is_premium_essence) == True does not work
    premium_essence_production = db.relationship(
        "Production",
        primaryjoin=(
            "foreign(Production.result_item_code) == "
            "Production.result_item_code"
        ),
        viewonly=True,
    )

    # Material 1
    material_1_code = CustomColumn(
        db.String(32), db.ForeignKey("item_list.code"),
        mapper_key="재료1",
        transform=lambda v: v if v != "#" else None)

    material_1_quantity = CustomColumn(
        db.Integer, mapper_key="재료1수량",
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
        db.Integer, mapper_key="재료2수량",
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
        db.Integer, mapper_key="재료3수량",
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
        db.Integer, mapper_key="재료4수량",
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
        db.Integer, mapper_key="재료5수량",
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
        db.Integer, mapper_key="재료6수량",
        transform=lambda v: v if v != 0 else None
    )

    material_6 = db.relationship("ItemList", foreign_keys=[material_6_code],
                                 viewonly=True,)

    def to_dict(
        self,
        minimal: bool = False,
        no_nested: bool = False
    ) -> dict:
        minimal_dict = {
            "code": self.code,
            "result_item": self.result_item.to_dict(with_item_data=True),
        }

        if minimal:
            return minimal_dict

        materials = []
        for i in range(1, 7):
            material_code = getattr(self, f"material_{i}_code")
            if material_code:
                materials.append({
                    "item":  getattr(self, f"material_{i}").to_dict(),
                    "quantity": getattr(self, f"material_{i}_quantity"),
                })

        # See FIXME at the column definition
        premium_production = next(
            filter(lambda p: p != self,
                   self.premium_essence_production),
            None)

        return {
            **minimal_dict,
            "production_type": self.production_type.to_dict(),
            "points_needed": self.points_needed,
            "result_item_quantity": self.result_item_quantity,
            "materials": materials,
            "premium_essence_production": (
                premium_production.to_dict(no_nested=True)
                if (premium_production and not no_nested)
                else None)
        }
