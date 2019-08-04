from app.extensions import db
from sqlalchemy.orm.collections import InstrumentedList
import json


class BaseModel(db.Model):
    __abstract__ = True

    _include_fields = []

    def to_dict(self, overview=False, includes=[]):
        """Return a dictionary representation of this model."""
        columns = self.__table__.columns.keys()
        relationships = self.__mapper__.relationships.keys()

        if overview:
            self.includes = self._include_fields
        else:
            self.includes = includes

        data = {}

        for column_name in columns:
            if not self.includes or column_name in self.includes:
                data[column_name] = getattr(self, column_name)

        for relationship_key in relationships:
            rel_data = self.get_relationship_data(parent_obj=self, relationship_key=relationship_key)
            if rel_data is not None:
                data[relationship_key] = rel_data

        return data

    def get_relationship_data(self, parent_obj, relationship_key, base_path=""):
        if base_path:
            _path = base_path + f".{relationship_key}"
        else:
            _path = relationship_key

        if self.includes and not any(include.startswith(_path) for include in self.includes):
            return None

        data = {}

        obj = getattr(parent_obj, relationship_key)

        if isinstance(obj, InstrumentedList) and obj:  # One to Many Relationship
            data_list = []

            for child_obj in obj:
                child_obj_data = {}

                obj_columns = child_obj.__table__.columns.keys()
                obj_relationships = child_obj.__mapper__.relationships.keys()

                for column_name in obj_columns:
                    _col_path = _path + f".{column_name}"
                    if not self.includes or _col_path in self.includes:
                        child_obj_data[column_name] = getattr(child_obj, column_name)

                for relationship_key in obj_relationships:
                    rel_data = self.get_relationship_data(
                        parent_obj=child_obj, relationship_key=relationship_key, base_path=_path)
                    if rel_data is not None:
                        child_obj_data[relationship_key] = rel_data

                data_list.append(child_obj_data)

            if not any(o for o in data_list):
                return []

            return data_list

        else:  # One to One Relationship
            if not hasattr(obj, "__table__"):
                return []

            obj_columns = obj.__table__.columns.keys()
            obj_relationships = obj.__mapper__.relationships.keys()

            for column_name in obj_columns:
                _col_path = _path + f".{column_name}"
                if not self.includes or _col_path in self.includes:
                    data[column_name] = getattr(obj, column_name)

            for relationship_key in obj_relationships:
                rel_data = self.get_relationship_data(
                    parent_obj=obj, relationship_key=relationship_key, base_path=_path)
                if rel_data is not None:
                    data[relationship_key] = rel_data

            if data:
                return data

            return []
