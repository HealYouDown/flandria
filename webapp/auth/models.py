from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from webapp.utils import get_current_time
from webapp import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = "user"
    __bind_key__ = "user_data"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    register_date = db.Column(db.DateTime, nullable=False, default=get_current_time)

    _is_admin = db.Column(db.Boolean, default=False)
    _can_edit_drops = db.Column(db.Boolean, default=False)
    _can_see_excludes = db.Column(db.Boolean, default=False)
    _can_see_users = db.Column(db.Boolean, default=False)
    _can_see_logs = db.Column(db.Boolean, default=False)
    _can_see_probability = db.Column(db.Boolean, default=False)
    _can_delete_builds = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User {}>'.format(self.username) 

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @property
    def is_admin(self):
        return self._is_admin

    @property
    def can_edit_drops(self):
        return self.is_admin or self._can_edit_drops

    @property
    def can_see_excludes(self):
        return self.is_admin or self._can_see_excludes

    @property
    def can_see_logs(self):
        return self.is_admin or self._can_see_logs
    
    @property
    def can_see_probability(self):
        return self.is_admin or self._can_see_probability

    @property
    def can_delete_builds(self):
        return self.is_admin or self._can_delete_builds


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


# Logs

class DropLog(db.Model):
    __tablename__ = "drop_log"
    __bind_key__ = "logs_data"
    index = db.Column(db.Integer, primary_key=True, autoincrement=True)

    action = db.Column(db.String)
    time = db.Column(db.DateTime, default=get_current_time)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", foreign_keys=[user_id])

    monster_code = db.Column(db.String, db.ForeignKey("monster.code"))
    monster = db.relationship("Monster", foreign_keys=[monster_code])

    item_code = db.Column(db.String, db.ForeignKey("item_list.code"))
    item = db.relationship("ItemList", foreign_keys=[item_code])
