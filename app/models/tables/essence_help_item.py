from app.extensions import db
from app.models.mixins import BaseMixin
from sqlalchemy import Column, String

class EssenceHelpItem(db.Model, BaseMixin):
    __tablename__ = "essence_help_item"
    __bind_key__ = "static_data"

    description = Column(String)

    def to_dict(self, minimal: bool = False) -> dict:
        return {
            **BaseMixin.to_dict(self, minimal),
            "description": self.description
        }
