from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from ...extensions import db
from ..mixins import BaseMixin
from .recipe import Recipe  # noqa F401


class Material(db.Model, BaseMixin):
    __tablename__ = "material"
    __bind_key__ = "static_data"

    produced_by_code = Column(String, ForeignKey('recipe.code'))
    produced_by = relationship("Recipe")

    def to_dict(self, minimal: bool = False) -> dict:
        return BaseMixin.to_dict(self, minimal)
