from app.extensions import db
from werkzeug.security import check_password_hash, generate_password_hash
from app.utils import get_current_time


class User(db.Model):
    __tablename__ = "user"
    __bind_key__ = "user_data"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(256), unique=True)
    email = db.Column(db.String(256), unique=True)
    password = db.Column(db.String(256))
    register_date = db.Column(db.DateTime, default=get_current_time)

    _admin = db.Column(db.Boolean, default=False)
    _can_edit_drops = db.Column(db.Boolean, default=False)
    _can_see_hidden = db.Column(db.Boolean, default=False)
    _can_see_users = db.Column(db.Boolean, default=False)
    _can_see_logs = db.Column(db.Boolean, default=False)
    _can_delete_planner_builds = db.Column(db.Boolean, default=False)

    @property
    def admin(self):
        return self._admin

    @property
    def can_edit_drops(self):
        return self.admin or self._can_edit_drops

    @property
    def can_see_hidden(self):
        return self.admin or self._can_see_hidden

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def rolenames(self):
        roles = []
        if self.admin:
            roles.append("admin")
        if self.can_edit_drops:
            roles.append("can_edit_drops")
        if self.can_see_hidden:
            roles.append("can_see_hidden")
        return roles

    @classmethod
    def lookup(cls, username):
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id):
        return cls.query.get(id)

    @property
    def identity(self):
        return self.id
