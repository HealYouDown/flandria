from dataclasses import dataclass, field
from itertools import chain
from typing import TYPE_CHECKING, Callable, Iterable, Sequence, Union

if TYPE_CHECKING:
    from src.updater.strategies.types import T_STRATEGY_FUNCTION


@dataclass
class RequiredFiles:
    server_files: Sequence[str] = field(default_factory=list)
    client_files: Sequence[str] = field(default_factory=list)
    string_files: Sequence[str] = field(default_factory=list)
    description_files: Sequence[str] = field(default_factory=list)
    extra_files: Sequence[str] = field(default_factory=list)

    @property
    def all_files(self) -> Iterable[str]:
        return chain(
            self.server_files,
            self.client_files,
            self.string_files,
            self.description_files,
            self.extra_files,
        )


@dataclass
class LoaderInfo:
    # Shortcut to use LoaderInfo.Files in declarations
    Files = RequiredFiles

    files: RequiredFiles
    loader_strategy: Union["T_STRATEGY_FUNCTION", None] = None
    row_filters: list[Callable[[dict], bool]] = field(default_factory=list)
    include_in_itemlist: bool = False
