import typing

from sqlalchemy import Column


class CustomColumn(Column):
    """Custom Column implementation that also asks for a 'mapper_key' which is
    used to map the data from the patchserver files to the model."""
    def __init__(
        self,
        *args,
        mapper_key: typing.Optional[str] = None,
        transform: typing.Optional[typing.Callable] = None,
        **kwargs,
    ):
        """Constructor for creating the custom column. Usage is the same as
        normal Column, however, a 'mapper_key' is required.

        Args:
            mapper_key (typing.Optional[str], optional): Key to map file
                columns to model. Defaults to None.
            transform (typing.Optional[typing.Callable], optional): Function
                to apply on the value (e.g. convert it to string). Defaults to
                None.

        Raises:
            ValueError: Is raised when 'mapper_key' is not specific.
        """
        super(CustomColumn, self).__init__(*args, **kwargs)
        self.mapper_key = mapper_key
        self.transform = transform
