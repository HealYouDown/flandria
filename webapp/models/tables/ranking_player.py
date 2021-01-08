from webapp.extensions import db
from webapp.models.enums import CharacterClass, Server
from webapp.utils import get_utc_now


class RankingPlayer(db.Model):
    __tablename__ = "ranking_player"

    # Unique key consists of servername_username, both case insensitive
    # e.g. bergruen_Shadow or luxplena_Shadow
    # Used to filter later
    composite_key_string = db.Column(db.String(32), nullable=False)

    # Use server and name as primary key, as duplicates are allowed.
    # You can have a Shadow on Bergruen and a Shadow on LuxPlena, *sometimes*.
    # Florensia race conditions I guess.
    server = db.Column(db.Enum(Server), nullable=False, primary_key=True)
    name = db.Column(db.String(32), nullable=False, primary_key=True)

    rank = db.Column(db.Integer, nullable=False)
    guild = db.Column(db.String(32))
    character_class = db.Column(db.Enum(CharacterClass), nullable=False)

    level_land = db.Column(db.Integer, nullable=False)
    level_sea = db.Column(db.Integer, nullable=False)

    updated_at = db.Column(db.DateTime, onupdate=get_utc_now)
    indexed_at = db.Column(db.DateTime, default=get_utc_now)
