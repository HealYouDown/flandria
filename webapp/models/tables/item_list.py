from webapp.extensions import db
import json


class ItemList(db.Model):
    __tablename__ = "item_list"

    code = db.Column(db.String(32),
                     primary_key=True)

    name = db.Column(db.String(256),
                     nullable=False,
                     index=True)

    icon = db.Column(db.String(32),
                     nullable=False)

    table = db.Column(db.String(64),
                      nullable=False)

    rare_grade = db.Column(db.Integer,
                           nullable=False,
                           default=0)

    duration = db.Column(db.Float)

    # All item data encoded as json
    item_data = db.Column(db.Text, nullable=False)

    def to_dict(self, with_item_data: bool = False) -> dict:
        minimal_dict = {
            "code": self.code,
            "name": self.name,
            "icon": self.icon,
            "table": self.table,
            "rare_grade": self.rare_grade,
            "duration": self.duration,
        }

        if not with_item_data:
            return minimal_dict

        return {
            **minimal_dict,
            "item_data": json.loads(self.item_data),
        }
