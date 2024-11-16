from typing import Any, Generator, MutableMapping, Optional, TypeVar

# Stolen and adapted from https://github.com/psf/requests/blob/main/requests/structures.py

V = TypeVar("V")


class CaseInsensitiveDict(MutableMapping[str, V]):
    def __init__(self, data: Optional[dict] = None, **kwargs):
        self._store: dict[str, tuple[str, Any]] = dict()
        if data is None:
            data = {}
        self.update(data, **kwargs)

    def __setitem__(self, key: str, value: Any) -> None:
        self._store[key.lower()] = (key, value)

    def __getitem__(self, key: Optional[str]) -> Any:
        if key is None:
            raise KeyError
        return self._store[key.lower()][1]

    def __delitem__(self, key: str) -> None:
        del self._store[key.lower()]

    def __iter__(self) -> Generator[str, None, None]:
        return (key for key, _ in self._store.values())

    def __len__(self) -> int:
        return len(self._store)

    def __repr__(self) -> str:
        return str(dict(self.items()))
