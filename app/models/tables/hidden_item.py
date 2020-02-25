from sqlalchemy import Column, String
from ...extensions import db


class HiddenItem(db.Model):
    __tablename__ = "hidden_item"
    __bind_key__ = "unstatic_data"

    code = Column(String, primary_key=True)

    def to_dict(self, minimal: bool = False) -> dict:
        return {
            "code": self.code,
        }
