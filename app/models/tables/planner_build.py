from app.extensions import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.models import User
import datetime

class PlannerBuild(db.Model):
    __tablename__ = "planner_build"
    __bind_key__ = "unstatic_data"

    index = Column(Integer, primary_key=True, autoincrement=True)
    planner_class = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", foreign_keys=[user_id])

    build_name = Column(String, nullable=False)
    build_description = Column(Text, nullable=False)
    selected_class = Column(String, nullable=True)
    selected_level = Column(Integer, nullable=False)

    hash = Column(String, nullable=False)

    stars = relationship("PlannerBuildStar", cascade="all, delete-orphan", lazy="joined")

    def to_dict(self) -> dict:
        return {
            "id": self.index,
            "created_at": str(self.created_at),
            "user": self.user.to_dict(),
            "build_name": self.build_name,
            "build_description": self.build_description,
            "planner_class": self.planner_class,
            "selected_class": self.selected_class,
            "selected_level": self.selected_level,
            "hash": self.hash,
            "stars": [star.to_dict() for star in self.stars]
        }


class PlannerBuildStar(db.Model):
    __tablename__ = "planner_build_star"
    __bind_key__ = "unstatic_data"

    index = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("user.id"))
    build_id = Column(Integer, ForeignKey("planner_build.index"))

    def to_dict(self):
        return {
            "id": self.index,
            "user_id": self.user_id,
            "build_id": self.build_id,
        }