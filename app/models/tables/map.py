from sqlalchemy import Column, String, Float
from ...extensions import db


class Map(db.Model):
    __tablename__ = "map"
    __bind_key__ = "static_data"

    code = Column(String, primary_key=True)
    name = Column(String)

    left = Column(Float)
    top = Column(Float)
    width = Column(Float)
    height = Column(Float)

    def to_dict(self, minimal: bool = False) -> dict:
        return {
            "code": self.code,
            "name": self.name,
            "left": self.left,
            "top": self.top,
            "width": self.width,
            "height": self.height,
        }
