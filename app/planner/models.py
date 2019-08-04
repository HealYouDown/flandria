from app.base_model import BaseModel
from app.extensions import db
from app.utils import get_current_time


class ShipSkill(BaseModel):
    __tablename__ = "ship_skill"
    __bind_key__ = "static_florensia_data"

    code = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    icon = db.Column(db.String)

    class_land = db.Column(db.String)
    skill_code = db.Column(db.String)
    skill_level = db.Column(db.Integer)

    required_level = db.Column(db.Integer)
    required_weapon = db.Column(db.String)

    mana_consumption = db.Column(db.Integer)
    cooldown = db.Column(db.Integer)
    description = db.Column(db.Text)

    required_skill_1 = db.Column(db.String)
    required_skill_2 = db.Column(db.String)
    required_skill_3 = db.Column(db.String)
    required_skill_4 = db.Column(db.String)
    required_skill_5 = db.Column(db.String)

    max_level = db.Column(db.Integer)


class PlayerSkill(BaseModel):
    __tablename__ = "player_skill"
    __bind_key__ = "static_florensia_data"

    code = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    icon = db.Column(db.String)

    class_land = db.Column(db.String)
    skill_code = db.Column(db.String)
    skill_level = db.Column(db.Integer)

    required_level = db.Column(db.Integer)
    required_weapon = db.Column(db.String)

    mana_consumption = db.Column(db.Integer)
    cooldown = db.Column(db.Integer)
    description = db.Column(db.Text)

    required_skill_1 = db.Column(db.String)
    required_skill_2 = db.Column(db.String)
    required_skill_3 = db.Column(db.String)
    required_skill_4 = db.Column(db.String)
    required_skill_5 = db.Column(db.String)

    max_level = db.Column(db.Integer)


class UserBuild(BaseModel):
    __tablename__ = "user_build"
    __bind_key__ = "unstatic_florensia_data"
    index = db.Column(db.Integer, primary_key=True, autoincrement=True)

    time = db.Column(db.DateTime, default=get_current_time)
    public = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", foreign_keys=[user_id])

    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text(200), nullable=False)

    class_ = db.Column(db.String, nullable=False)

    selected_class = db.Column(db.String, nullable=False)
    selected_level = db.Column(db.Integer, nullable=False)

    hash = db.Column(db.String, nullable=False)

    stars = db.relationship("UserBuildStar", cascade="all, delete-orphan")
    stars_count = db.Column(db.Integer, default=0)


class UserBuildStar(BaseModel):
    __tablename__ = "user_build_star"
    __bind_key__ = "unstatic_florensia_data"
    index = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", foreign_keys=[user_id])

    build_id = db.Column(db.Integer, db.ForeignKey("user_build.index"))
