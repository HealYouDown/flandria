from typing import Any, Type


def get_immediate_mixin_classes(cls: Type[Any]) -> list[Type[Any]]:
    bases: list[type] = []
    for base in cls.__bases__:
        if not base.__module__.startswith("src.database.mixins"):
            continue
        bases.append(base)

    return bases


def get_all_mixin_base_classes(cls: Type[Any]) -> list[Type[Any]]:
    bases: list[type] = []
    for base in cls.__bases__:
        if not base.__module__.startswith("src.database.mixins"):
            continue
        bases.append(base)
        bases.extend(get_all_mixin_base_classes(base))
    return bases
