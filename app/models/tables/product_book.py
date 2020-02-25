from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from ...extensions import db
from ..mixins import BaseMixin


class ProductBook(db.Model, BaseMixin):
    __tablename__ = "product_book"
    __bind_key__ = "static_data"

    target_code = Column(String, ForeignKey("production.code"))
    target = relationship("Production",
                          foreign_keys=[target_code],
                          lazy="joined")

    def to_dict(
        self,
        minimal: bool = False,
        as_needed_for: bool = False
    ) -> dict:
        if as_needed_for:
            return BaseMixin.to_dict(self, True)

        return {
            **BaseMixin.to_dict(self, minimal),
            "production": self.target.to_dict(minimal)
        }
