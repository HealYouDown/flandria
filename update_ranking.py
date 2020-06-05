import hashlib
import json
import sys

from app import create_app
from app.extensions import db
from app.models import Guild, Player

PLAYER_JSON_FILE = sys.argv[1]

if __name__ == "__main__":
    app = create_app(development=False)

    with open(PLAYER_JSON_FILE, "r") as fp:
        players = json.load(fp)

    with app.app_context():
        db.drop_all(bind="ranking")
        db.create_all(bind="ranking")

        db.session.bulk_insert_mappings(Player, players)
        db.session.flush()

        guilds = set((player.guild, player.server)
                    for player in db.session.query(Player).filter(Player.guild.isnot(None)).all())

        guild_data = [{"id": index,
                    "name": guild[0],
                    "server": guild[1],
                    "name_hash": hashlib.md5(guild[0].encode()).hexdigest(),
                    } for index, guild in enumerate(guilds)
                    ]

        for guild in guild_data:
            guild_members = [p for p in players if p["guild"] == guild["name"]]
            guild["number_of_members"] = len(guild_members)
            guild["avg_rank"] = sum([p["rank"] for p in guild_members]) / len(guild_members)

        db.session.bulk_insert_mappings(Guild, guild_data)

        db.session.commit()
