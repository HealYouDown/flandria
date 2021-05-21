from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

"""
Example:

class Material(db.Model, BaseMixin, DroppedByMixin, ProducedByMixin,
               NeededForMixin, ...):
    __tablename__ = "material"

    ...
"""


@as_declarative()
class ItemSetMixin:
    @declared_attr
    def item_set(cls):
        columns = ["weapon_code", "coat_code", "pants_code",
                   "shoes_code", "gauntlet_code", "shield_code",
                   "necklace_code", "earring_code", "ring_1_code",
                   "ring_2_code", "dress_code", "hat_code"]

        join = ",".join(
            f"foreign(ItemSet.{column}) == {cls.__name__}.code"
            for column in columns
        )

        return relationship(
            "ItemSet",
            uselist=False,
            primaryjoin=f"or_({join})",
            viewonly=True,
        )

    def to_dict(self) -> dict:
        if self.item_set is None:
            return {
                "item_set": None,
            }

        return {
            "item_set": self.item_set.to_dict(),
        }


@as_declarative()
class UpgradeRuleMixin:
    @declared_attr
    def upgrade_rule(cls):
        return relationship(
            "UpgradeRule",
            order_by="asc(UpgradeRule.upgrade_level)",
            primaryjoin=("foreign(UpgradeRule.code) == "
                         f"{cls.__name__}.upgrade_code"),
            viewonly=True,
        )

    def to_dict(self) -> dict:
        return {
            "upgrade_rule": [rule.to_dict() for rule in self.upgrade_rule],
        }


@as_declarative()
class DroppedByMixin:
    @declared_attr
    def dropped_by(cls):
        return relationship(
            "Drop",
            primaryjoin=f"foreign(Drop.item_code) == {cls.__name__}.code",
            viewonly=True,
        )

    def to_dict(self) -> dict:
        return {
            "dropped_by": [drop.to_dict(monster_dict=True)
                           for drop in self.dropped_by]
        }


@as_declarative()
class ProducedByMixin:
    @declared_attr
    def produced_by_recipe(cls):
        return relationship(
            "Recipe",
            primaryjoin=(
                f"foreign(Recipe.result_item_code) == {cls.__name__}.code"),
            viewonly=True,
        )

    @declared_attr
    def produced_by_second_job(cls):
        return relationship(
            "Production",
            primaryjoin=(
                "and_(foreign(Production.result_item_code) == "
                f"{cls.__name__}.code, "
                "not_(foreign(Production.is_premium_essence)))"),
            viewonly=True,
        )

    def to_dict(self) -> dict:
        return {
            "produced_by": {
                "recipe": [item.to_dict()
                           for item in self.produced_by_recipe],
                "second_job": [item.to_dict()
                               for item in self.produced_by_second_job],
            },
        }


@as_declarative()
class NeededForMixin:
    @declared_attr
    def needed_for_recipe(cls):
        join = ",".join(
            f"foreign(Recipe.material_{i}_code) == {cls.__name__}.code"
            for i in range(1, 7))

        return relationship(
            "Recipe",
            primaryjoin=(f"or_({join})"),
            viewonly=True,
        )

    @declared_attr
    def needed_for_second_job(cls):
        join = ",".join(
            f"foreign(Production.material_{i}_code) == {cls.__name__}.code"
            for i in range(1, 7))

        return relationship(
            "Production",
            primaryjoin=(f"and_(or_({join}), "
                         "not_(foreign(Production.is_premium_essence)))"),
            viewonly=True,
        )

    def to_dict(self) -> dict:
        return {
            "needed_for": {
                "recipe": [item.to_dict()
                           for item in self.needed_for_recipe],
                "second_job": [item.to_dict()
                               for item in self.needed_for_second_job],
            },
        }


@as_declarative()
class RandomBoxMixin:
    @declared_attr
    def random_boxes(cls):
        join = ",".join(
            f"foreign(RandomBox.item_{i}_code) == {cls.__name__}.code"
            for i in range(0, 62))

        return relationship(
            "RandomBox",
            primaryjoin=(f"or_({join})"),
            viewonly=True,
        )

    def to_dict(self) -> dict:
        return {
            "random_boxes": [box.to_dict() for box in self.random_boxes],
        }


@as_declarative()
class SoldByMixin:
    @declared_attr
    def sold_by(cls):
        return relationship(
            "NpcShopItem",
            primaryjoin=("foreign(NpcShopItem.item_code) == "
                         f"{cls.__name__}.code"),
            viewonly=True,
        )

    def to_dict(self) -> dict:
        return {
            "sold_by": [shop_item.to_dict(npc_dict=True)
                        for shop_item in self.sold_by],
        }
