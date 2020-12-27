import json
import enum


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, enum.Enum):
            return obj.to_dict()

        return json.JSONEncoder.default(self, obj)
