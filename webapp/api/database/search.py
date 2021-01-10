from flask_restx import Resource
from sqlalchemy import or_
from webapp.api.utils import get_url_parameter
from webapp.models import ItemList, Monster, Npc, Quest, RankingPlayer


class Search(Resource):
    LIMIT = 15

    def get(self):
        search_string = get_url_parameter("s", str, None)
        if not search_string:
            return [], 200
        else:
            search_string = search_string.strip()

        items = (
            ItemList.query
            .filter(or_(
                ItemList.name.contains(search_string),
                ItemList.code.contains(search_string),
            )).limit(
                self.LIMIT
            ).all()
        )

        monsters = (
            Monster.query
            .filter(or_(
                Monster.name.contains(search_string),
                Monster.code.contains(search_string),
            )).limit(
                self.LIMIT
            ).all()
        )

        npcs = (
            Npc.query.filter(or_(
                Npc.name.contains(search_string),
                Npc.code.contains(search_string),
            )).limit(
                self.LIMIT
            ).all()
        )

        quests = (
            Quest.query.filter(or_(
                Quest.title.contains(search_string),
                Quest.code.contains(search_string),
            )).limit(
                self.LIMIT
            ).all()
        )

        guilds = (
            RankingPlayer.query.
            with_entities(
                RankingPlayer.guild,
                RankingPlayer.server,
            ).group_by(
                RankingPlayer.guild
            ).filter(
                RankingPlayer.guild.contains(search_string)
            ).limit(
                self.LIMIT
            ).all()
        )

        players = (
            RankingPlayer.query
            .filter(
                RankingPlayer.name.contains(search_string)
            ).order_by(
                RankingPlayer.rank,
            ).limit(
                self.LIMIT
            ).all()
        )

        resp = {}

        if monsters:
            resp["monsters"] = [monster.to_dict(minimal=True)
                                for monster in monsters]

        if items:
            resp["items"] = [item.to_dict(with_item_data=True)
                             for item in items]

        if npcs:
            resp["npcs"] = [npc.to_dict(minimal=True)
                            for npc in npcs]

        if quests:
            resp["quests"] = [quest.to_dict(minimal=True)
                              for quest in quests]

        if players:
            resp["players"] = [player.to_dict(minimal=True)
                               for player in players]

        if guilds:
            resp["guilds"] = [
                {
                    "name": guild.guild,
                    "server": guild.server.to_dict()
                } for guild in guilds
            ]

        return resp, 200
