import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.database.column_types import RGB


class FlorensiaModelMixin:
    model_name = orm.mapped_column(sa.String(16), nullable=True)

    @orm.declared_attr
    def models(cls):
        cls_name = cls.__name__  # type: ignore
        join = f"foreign(Available3DModel.model_name) == {cls_name}.model_name"

        if hasattr(cls, "model_variant"):
            variant_join = (
                f"foreign(Available3DModel.model_variant).is_({cls_name}.model_variant)"
            )
            join = f"and_({join}, {variant_join})"

        return orm.relationship(
            "Available3DModel", primaryjoin=join, uselist=True, viewonly=True
        )


class ActorModelMixin(FlorensiaModelMixin):
    # We don't do shit with scale right now, as we would have to
    # create a own export for each 3d model with a different scale
    # instead of just re-using the same one without changing scale.
    # Safes a lot of disk space that way.
    model_scale = orm.mapped_column(sa.Float, nullable=True)


class ExtraEquipmentModelMixin(FlorensiaModelMixin):
    # Variant is an RGB value that converts a specific mesh to a different color.
    # Used for the likes of Ribbon Hairbands, Hats, Robes, ...
    model_variant = orm.mapped_column(RGB, nullable=True)
