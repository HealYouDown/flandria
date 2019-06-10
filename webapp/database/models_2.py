from webapp import db
from webapp.utils import get_current_time


class ExcludeFromView(db.Model):
    __tablename__ = "exclude_from_view"
    __bind_key__ = "unstatic_florensia_data"
    item_code = db.Column(db.String, db.ForeignKey("item_list.code"), primary_key=True)
    item = db.relationship("ItemList", foreign_keys=[item_code])


class Drop(db.Model):
    __tablename__ = "drop"
    __bind_key__ = "unstatic_florensia_data"
    index = db.Column(db.Integer, primary_key=True, autoincrement=True)

    monster_code = db.Column(db.String, db.ForeignKey("monster.code"))
    monster = db.relationship("Monster", foreign_keys=[monster_code])

    item_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item = db.relationship("ItemList", foreign_keys=[item_code])


class DropMessage(db.Model):
    __tablename__ = "drop_message"
    __bind_key__ = "unstatic_florensia_data"

    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_time = db.Column(db.DateTime, default=get_current_time)

    declined = db.Column(db.Boolean, default=False)
    accepted = db.Column(db.Boolean, default=False)

    monster_code = db.Column(db.String, db.ForeignKey("monster.code"), nullable=False)
    monster = db.relationship("Monster", foreign_keys=[monster_code])

    message = db.Column(db.String, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", foreign_keys=[user_id])
