from flask import request
import typing
import json


def get_url_parameter(
    name: str,
    type_: typing.Any,
    default_value: typing.Any,
    validate: typing.Optional[typing.Callable] = None,
):
    value = request.args.get(name, default=default_value)

    # Give back default value with any checks.
    if value == default_value:
        return value

    # Perform type conversion.
    if type_ == int:
        value = int(value)
    elif type_ == bool:
        value = bool(int(value))
    elif type_ == list:
        try:
            value = json.loads(value)
        except json.decoder.JSONDecodeError:
            return default_value

    # Check if argument matches validate function, if given.
    if not validate:
        return value

    if validate(value):
        return value
    else:
        return default_value
