from sqlalchemy import Column, String, Integer
from ...extensions import db


class ItemList(db.Model):
    __tablename__ = "item_list"
    __bind_key__ = "static_data"

    code = Column(String, primary_key=True)
    name = Column(String)
    icon = Column(String)

    table = Column(String)
    rare_grade = Column(Integer, default=0)

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "name": self.name,
            "icon": self.icon,
            "table": self.table,
            "rare_grade": self.rare_grade
        }
