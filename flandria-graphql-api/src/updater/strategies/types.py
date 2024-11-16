from typing import TYPE_CHECKING, Callable, Sequence

if TYPE_CHECKING:
    from src.database.types import ModelCls
    from src.updater.schema import LoaderInfo


T_STRATEGY_RETURN = Sequence[
    tuple[
        ModelCls,
        list[dict],
    ]
]

T_STRATEGY_FUNCTION = Callable[
    [
        ModelCls,
        "LoaderInfo",
    ],
    T_STRATEGY_RETURN,
]
