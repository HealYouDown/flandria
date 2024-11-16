import enum
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from src.database import mixins as database_mixins
from src.database import models as database_models

from .helpers import get_all_mixin_base_classes, get_immediate_mixin_classes
from .inspector import InspectedORMField, inspect_model

if TYPE_CHECKING:
    from src.database.types import ModelCls


@dataclass
class MixinDeclaration:
    name: str
    fields: list[InspectedORMField]
    bases: list[str]


@dataclass
class ModelDeclaration:
    name: str
    fields: list[InspectedORMField]
    mixins: list[MixinDeclaration] = field(default_factory=list)

    # Mixins that the model inherits from, not including all mixins that the mixin inherits from.
    immediate_mixin_names: list[str] = field(default_factory=list)


def get_declarations() -> tuple[list[MixinDeclaration], list[ModelDeclaration]]:
    mixin_declarations: dict[type, MixinDeclaration] = {}
    model_declarations: dict[ModelCls, ModelDeclaration] = {}

    models: list[ModelCls] = map(database_models.__dict__.get, database_models.__all__)  # type: ignore
    for model_cls in models:
        fields = inspect_model(model_cls)
        mixins: list[MixinDeclaration] = []
        immediate_mixins_names = [
            o.__name__ for o in get_immediate_mixin_classes(model_cls)
        ]

        for mixin_cls in get_all_mixin_base_classes(model_cls):
            mixin_column_names = [
                key for key in mixin_cls.__dict__ if not key.startswith("__")
            ]

            # Due to the declared attributes on the mixins, we can't get the type from it.
            # We have to look up the column from the mixin in the model mapper.
            if mixin_cls in mixin_declarations:
                mixin = mixin_declarations[mixin_cls]
            else:
                mixin_fields = [f for f in fields if f.name in mixin_column_names]
                mixin = MixinDeclaration(
                    name=mixin_cls.__name__,
                    fields=mixin_fields,
                    bases=[o.__name__ for o in get_immediate_mixin_classes(mixin_cls)],
                )
                mixin_declarations[mixin_cls] = mixin

            mixins.append(mixin)

            # remove all fields from our model declaration that belong to the mixin
            fields = [f for f in fields if f.name not in mixin_column_names]

        model_declarations[model_cls] = ModelDeclaration(
            name=model_cls.__name__,
            fields=fields,
            mixins=mixins,
            immediate_mixin_names=immediate_mixins_names,
        )

    return list(mixin_declarations.values()), list(model_declarations.values())


def generate_strawberry_input_filters() -> str:
    mixins, models = get_declarations()

    scalar_filter_name_lookup = {
        int: "NumberFilter",
        float: "NumberFilter",
        str: "StringFilter",
        bool: "BooleanFilter",
    }

    contents = """
from typing import Optional

import strawberry

from src.api import enums

from .scalar_filters import BooleanFilter, EnumFilter, NumberFilter, StringFilter
"""

    for mixin in mixins:
        mixin_str = f"@strawberry.input\nclass {mixin.name}Filter:\n"
        filtered_fields = [f for f in mixin.fields if not f.exclude_from_filters]

        if filtered_fields:
            for f in filtered_fields:
                if f.annotation_requires_forwardref:
                    filter = f'"{f.type_.__name__}Filter"'
                else:
                    if issubclass(f.type_, enum.Enum):
                        filter = f"EnumFilter[enums.{f.type_.__name__}]"
                    else:
                        filter = scalar_filter_name_lookup[f.type_]  # type: ignore

                mixin_str += "\t" + f"{f.name}: Optional[{filter}] = strawberry.UNSET\n"
        else:
            mixin_str += "\t...\n"

        contents += mixin_str

    for model in models:
        mixin_bases = ", ".join(f"{m.name }Filter" for m in model.mixins)
        model_str = f"@strawberry.input\nclass {model.name}Filter({mixin_bases}):\n"
        filtered_fields = [f for f in model.fields if not f.exclude_from_filters]

        if filtered_fields:
            for f in filtered_fields:
                if f.annotation_requires_forwardref:
                    filter = f'"{f.type_.__name__}Filter"'
                else:
                    if issubclass(f.type_, enum.Enum):
                        filter = f"EnumFilter[enums.{f.type_.__name__}]"
                    else:
                        filter = scalar_filter_name_lookup[f.type_]  # type: ignore

                model_str += "\t" + f"{f.name}: Optional[{filter}] = strawberry.UNSET\n"
        else:  # handle models that only inherit from mixin and don't declare any fields themselves
            model_str += "\t...\n"
        # model_str += "\n"
        # for key in ("AND", "OR", "NOT"):
        #     model_str += "\t" + f"{key}: Optional[list[Self]] = strawberry.UNSET\n"

        contents += model_str

    return contents


def generate_strawberry_sort_inputs() -> str:
    mixins, models = get_declarations()

    contents = """
from typing import Optional

import strawberry

from .sort_direction import SortDirection
"""

    for mixin in mixins:
        mixin_str = f"@strawberry.input\nclass {mixin.name}Sort:\n"

        # We don't support enums or relationships for sorting
        filtered_mixin_fields = [
            field
            for field in mixin.fields
            if not (
                issubclass(field.type_, enum.Enum)
                or field.annotation_requires_forwardref
            )
            or field.exclude_from_filters
        ]
        if filtered_mixin_fields:
            for f in filtered_mixin_fields:
                mixin_str += (
                    "\t" + f"{f.name}: Optional[SortDirection] = strawberry.UNSET\n"
                )
        else:
            mixin_str += "\t...\n"
        contents += mixin_str

    for model in models:
        mixin_bases = ", ".join(f"{m.name}Sort" for m in model.mixins)
        model_str = (
            f"@strawberry.input(one_of=True)\nclass {model.name}Sort({mixin_bases}):\n"
        )

        # We don't support enums or relationships for sorting
        filtered_model_fields = [
            field
            for field in model.fields
            if not (
                issubclass(field.type_, enum.Enum)
                or field.annotation_requires_forwardref
            )
            or field.exclude_from_filters
        ]
        if filtered_model_fields:
            for f in filtered_model_fields:
                model_str += (
                    "\t" + f"{f.name}: Optional[SortDirection] = strawberry.UNSET\n"
                )
        else:
            model_str += "\t...\n"
        contents += model_str

    return contents


def generate_strawberry_models() -> str:
    mixins, models = get_declarations()

    contents = """
from typing import Optional

import strawberry

from src.api import enums
"""

    # It's a lot easier to just sort the mixins manually instead of coming up
    # with a clever function using trees / graphs that lists them in order..
    mixin_order = [
        # Mixins without any bases
        database_mixins.RowIDMixin,
        database_mixins.FlorensiaModelMixin,
        database_mixins.EffectMixin,
        database_mixins.ClassLandMixin,
        database_mixins.ClassSeaMixin,
        database_mixins.ItemSetMixin,
        database_mixins.UpgradeRuleMixin,
        # Rest
        database_mixins.BaseMixin,
        database_mixins.SkillMixin,
        database_mixins.WeaponMixin,
        database_mixins.ArmorMixin,
        database_mixins.EquipmentMixin,
        database_mixins.ActorModelMixin,
        database_mixins.ExtraEquipmentModelMixin,
        database_mixins.ShipBaseMixin,
        database_mixins.ActorMixin,
    ]
    mixin_order_names: list[str] = [m.__name__ for m in mixin_order]
    assert all(
        m.name in mixin_order_names for m in mixins
    ), "Missing mixin in sorted mixin list for codegen"

    mixin_declarations_sorted = sorted(
        mixins, key=lambda m: mixin_order_names.index(m.name)
    )

    for mixin in mixin_declarations_sorted:
        mixin_str = (
            f"@strawberry.interface\nclass {mixin.name}({', '.join(mixin.bases)}):\n"
        )
        for f in mixin.fields:
            mixin_str += "\t" + f"{f.name}: {f.strawberry_annotation}\n"
        contents += mixin_str

    for model in models:
        model_bases = ", ".join(model.immediate_mixin_names)
        model_str = f"@strawberry.type\nclass {model.name}({model_bases}):\n"
        if model.fields:
            for f in model.fields:
                model_str += "\t" + f"{f.name}: {f.strawberry_annotation}\n"
        else:  # handle models that only inherit from mixin and don't declare any fields themselves
            model_str += "\t...\n"
        contents += model_str

    return contents
