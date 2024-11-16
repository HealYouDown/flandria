from typing import TYPE_CHECKING, Optional, Self

if TYPE_CHECKING:
    from src.updater.transforms.types import T_TRANSFORM_FUNCTION


class ColumnInfo(dict):
    def __init__(
        self,
        key: str,
        transforms: Optional[list["T_TRANSFORM_FUNCTION"]] = None,
        icon_key: Optional[str] = None,
        description_key: Optional[str] = None,
    ) -> None:
        """Contains information on how the default loading strategy matches the
        data from the client to the columns.

        Args:
            key (str): Key in the client file (Some korean shit)
            transforms (Optional[list["T_TRANSFORM_FUNCTION"]], optional): List of transform functions that are applied to the value. Defaults to None.
            icon_key (Optional[str], optional): Icon Key. Defaults to None.
            description_key (Optional[str], optional): Description Key. Defaults to None.
        """
        super().__init__()
        self.update(
            {
                "key": key,
                "transforms": transforms if transforms else [],
                "icon_key": icon_key,
                "description_key": description_key,
            }
        )

    @classmethod
    def code(cls) -> Self:
        return cls(key="코드")

    @classmethod
    def name(cls) -> Self:
        return cls(key="__name")

    @classmethod
    def icon(cls, icon_key: str = "아이콘") -> Self:
        return cls(key="__icon", icon_key=icon_key)

    @classmethod
    def description(cls, description_key: str = "코드") -> Self:
        return cls(key="__description", description_key=description_key)
