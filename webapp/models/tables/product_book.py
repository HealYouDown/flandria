from webapp.extensions import db
from webapp.models.declarative_mixins import SoldByMixin
from webapp.models.mixins import BaseMixin
from webapp.models.custom_sql_classes import CustomColumn


class ProductBook(
    db.Model, BaseMixin,
    SoldByMixin
):
    __tablename__ = "product_book"

    _mapper_utils = {
        "files": {
            "server": [
                "s_ProductBook.bin"
            ],
            "client": [
                "c_ProductRes.bin"
            ],
            "string": [
                "ProductStr.dat"
            ],
        },
    }

    production_code = CustomColumn(
        db.String(32), db.ForeignKey("production.code"),
        nullable=False, mapper_key="대상코드")

    production = db.relationship("Production", foreign_keys=[production_code],
                                 uselist=False, viewonly=True)

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = BaseMixin.to_dict(self, minimal)

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "production": self.production.to_dict(minimal=True),
            **SoldByMixin.to_dict(self),
        }
