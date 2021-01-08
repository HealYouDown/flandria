from webapp.extensions import db
from webapp.models.enums import CharacterClass, Server
from webapp.utils import get_utc_now


class RankingPlayerHistory(db.Model):
    __tablename__ = "ranking_player_history"

    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    server = db.Column(db.Enum(Server), nullable=False)
    name = db.Column(db.String(16), nullable=False)

    previous_level_land = db.Column(db.Integer)
    new_level_land = db.Column(db.Integer)

    previous_level_sea = db.Column(db.Integer)
    new_level_sea = db.Column(db.Integer)

    previous_character_class = db.Column(db.Enum(CharacterClass))
    new_character_class = db.Column(db.Enum(CharacterClass))

    previous_guild = db.Column(db.String(16))
    new_guild = db.Column(db.String(16))

    inserted_at = db.Column(db.DateTime, default=get_utc_now)
