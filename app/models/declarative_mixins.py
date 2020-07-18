from sqlalchemy.ext.declarative.api import as_declarative
from sqlalchemy.ext.declarative.base import declared_attr
from sqlalchemy.orm import relationship

"""
Example:

class Material(db.Model, BaseMixin, DroppedByMixin, ProducedByMixin,
               NeededForMixin):
    __tablename__ = "material"
    __bind_key__ = "static_data"

    produced_by_code = Column(String, ForeignKey('recipe.code'))
    produced_by = relationship("Recipe")

"""

# TODO: Rewrite API in detailed_view to use declarative mixins
# instead of querying all extras singlely.

@as_declarative()
class DroppedByMixin:
    @declared_attr
    def dropped_by(cls):
        return relationship(
            "Drop",
            primaryjoin=f"foreign(Drop.item_code) == {cls.__name__}.code"
        )


@as_declarative()
class ProducedByMixin:
    @declared_attr
    def produced_by_recipe(cls):
        return relationship(
            "Recipe",
            primaryjoin=f"foreign(Recipe.result_code) == {cls.__name__}.code"
        )

    @declared_attr
    def produced_by_2nd_job(cls):
        return relationship(
            "Production",
            primaryjoin=f"foreign(Production.result_code) == {cls.__name__}.code"
        )


@as_declarative()
class NeededForMixin:
    @declared_attr
    def needed_for_recipe(cls):
        name = cls.__name__

        return relationship(
            "Recipe",
            primaryjoin=(
                "or_("
                f"foreign(Recipe.material_1_code) == {name}.code,"
                f"foreign(Recipe.material_2_code) == {name}.code,"
                f"foreign(Recipe.material_3_code) == {name}.code,"
                f"foreign(Recipe.material_4_code) == {name}.code,"
                f"foreign(Recipe.material_5_code) == {name}.code,"
                f"foreign(Recipe.material_6_code) == {name}.code"
                ")"
            )
        )

    @declared_attr
    def needed_for_2nd_job(cls):
        name = cls.__name__

        return relationship(
            "Production",
            primaryjoin=(
                "or_("
                f"foreign(Production.material_1_code) == {name}.code,"
                f"foreign(Production.material_2_code) == {name}.code,"
                f"foreign(Production.material_3_code) == {name}.code,"
                f"foreign(Production.material_4_code) == {name}.code,"
                f"foreign(Production.material_5_code) == {name}.code,"
                f"foreign(Production.material_6_code) == {name}.code"
                ")"
            )
        )

