from webapp.models.enums import CharacterClass
from webapp.extensions import db
from webapp.utils import get_utc_now


class PlannerBuild(db.Model):
    __tablename__ = "planner_build"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", foreign_keys=[user_id],
                           viewonly=True,)

    created_at = db.Column(db.DateTime, default=get_utc_now)

    character_class = db.Column(db.Enum(CharacterClass), nullable=False)
    build_hash = db.Column(db.String(128), nullable=False)
    build_title = db.Column(db.String(128), nullable=False)
    build_description = db.Column(db.Text(1024), nullable=False)

    stars = db.relationship("PlannerStar", lazy="joined", cascade="all,delete")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user": self.user.to_dict(),
            "created_at": str(self.created_at),
            "character_class": self.character_class.to_dict(),
            "build_hash": self.build_hash,
            "build_title": self.build_title,
            "build_description": self.build_description,
            "stars": [star.to_dict() for star in self.stars]
        }


class PlannerStar(db.Model):
    __tablename__ = "planner_star"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    build_id = db.Column(db.Integer, db.ForeignKey("planner_build.id"),
                         nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    created_at = db.Column(db.DateTime, default=get_utc_now)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "created_at": str(self.created_at),
        }
