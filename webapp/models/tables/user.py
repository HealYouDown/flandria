from webapp.extensions import db
from webapp.utils import get_utc_now
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(2048), nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=get_utc_now)
    updated_at = db.Column(db.DateTime, onupdate=get_utc_now)

    admin = db.Column(db.Boolean, default=False)
    can_edit_drops = db.Column(db.Boolean, default=False)
    premium = db.Column(db.Boolean, default=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
        }

    def get_jwt_content(self) -> dict:
        """Returns the content that is included in the JWT.

        Returns:
            dict: dict with string string pairs.
        """
        return {
            "id": self.id,
            "username": self.username,
            "admin": self.admin,
            "can_edit_drops": self.admin or self.can_edit_drops,
            "premium": self.admin or self.premium,
        }

    def set_password(self, password: str) -> None:
        """Sets a password has from the given password to the user object.

        Args:
            password (str): The password to set.
        """
        pw_hash = generate_password_hash(password)
        self.password = pw_hash

    def check_password(self, password) -> bool:
        """Compares user password hash to given password

        Args:
            password (str): Given user password.

        Returns:
            bool: True if passwords match, False if not.
        """
        return check_password_hash(self.password, password)
