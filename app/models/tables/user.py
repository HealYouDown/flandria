import datetime

from sqlalchemy import Boolean, Column, Integer, String, DateTime
from werkzeug.security import check_password_hash, generate_password_hash

from ...extensions import db


class User(db.Model):
    __tablename__ = "user"
    __bind_key__ = "user_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(128), nullable=False, unique=True)
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(2048), nullable=False)
    register_date = Column(DateTime, nullable=False,
                           default=datetime.datetime.utcnow)

    admin = Column(Boolean, default=False)
    can_edit_drops = Column(Boolean, default=False)
    can_see_hidden = Column(Boolean, default=False)
    can_see_probability = Column(Boolean, default=False)

    def set_password(self, password) -> None:
        pw_hash = generate_password_hash(password)
        self.password = pw_hash

    def check_password(self, password) -> bool:
        return check_password_hash(self.password, password)

    @property
    def is_admin(self) -> bool:
        return self.admin

    @property
    def is_able_to_edit_drops(self) -> bool:
        return self.admin or self.can_edit_drops

    @property
    def is_able_to_see_hidden(self) -> bool:
        return self.admin or self.can_see_hidden

    @property
    def is_able_to_see_probability(self) -> bool:
        return self.admin or self.can_see_probability
