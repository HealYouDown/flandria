from typing import TYPE_CHECKING

from src.database.mixins import (
    ActorModelMixin,
    ClassLandMixin,
    ClassSeaMixin,
    EffectMixin,
    ExtraEquipmentModelMixin,
    FlorensiaModelMixin,
)
from src.updater.file_data import FileData
from src.updater.helpers import (
    get_actor_model_info,
    get_class_land,
    get_class_sea,
    get_effects,
    get_extra_equipment_model_info,
    get_model_info,
    map_row_to_model,
)

if TYPE_CHECKING:
    from src.database.types import ModelCls
    from src.updater.schema import LoaderInfo

    from .types import T_STRATEGY_RETURN


def default(
    model_cls: "ModelCls",
    loader_info: "LoaderInfo",
) -> "T_STRATEGY_RETURN":
    from src.database.models import Effect

    # Load data for all given files
    data = FileData.from_files(loader_info.files)

    objects = []
    effects = []
    for row in data.server_data:
        if not all(filter_fn(row) for filter_fn in loader_info.row_filters):
            continue

        pk, obj = map_row_to_model(model_cls, row, data)

        # Handle inherited mixin classes that need attributes set
        mros = model_cls.mro()
        if ClassLandMixin in mros:
            obj.update(get_class_land(row, model_cls.__tablename__))
        if ClassSeaMixin in mros:
            obj.update(get_class_sea(row, model_cls.__tablename__))
        if EffectMixin in mros:
            assert pk is not None
            effects.extend(get_effects(row, model_cls.__tablename__, pk))

        # 3D-Model things
        if FlorensiaModelMixin in mros:
            assert pk is not None
            obj.update(get_model_info(pk, data))
        if ActorModelMixin in mros:
            assert pk is not None
            obj.update(get_actor_model_info(pk, data))
        if ExtraEquipmentModelMixin in mros:
            assert pk is not None
            obj.update(get_extra_equipment_model_info(pk, data))

        objects.append(obj)

    return [
        (model_cls, objects),
        (Effect, effects),
    ]
