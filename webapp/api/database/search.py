import re
import typing

from flask_restx import Resource
from sqlalchemy import or_
from webapp.api.utils import get_url_parameter
from webapp.models import ItemList, Monster, Npc, Quest, RankingPlayer


class Search(Resource):
    def get(self):
        search_string = get_url_parameter("s", str, None)
        if not search_string:
            return [], 200
        else:
            search_string = search_string.strip()

        # Check if search string is in a format that is used to parse for
        # exact columns, e.g. key1:value1 key2:value2 ..
        column_filters = list(re.findall(r"(\w+):([^\s]+)", search_string))
        if column_filters:
            resp = self._handle_column_search(column_filters)
        else:
            resp = self._handle_normal_search(search_string)

        return resp

    def _handle_column_search(
        self,
        column_filters: typing.List[typing.Tuple[str, str]],
        limit: int = 50,
    ):
        queries = [
            ("monsters", Monster),
            ("items", ItemList),
            ("npcs", Npc),
            ("quests", Quest,),
            ("players", RankingPlayer)
        ]

        resp = {}

        for resp_key, table in queries:
            query = table.query
            skip: bool = False

            for column_key, value in column_filters:
                if hasattr(table, column_key):
                    column = getattr(table, column_key)

                    try:  # Check if value is a number
                        value = float(value)
                        query = query.filter(column == value)
                    except ValueError:  # string
                        # replace _ in strings with space
                        value = value.replace("_", " ")
                        query = query.filter(column.contains(value))
                else:
                    skip = True
                    break

            if not skip:
                obj_kws = (
                    {"minimal": True} if resp_key != "items"
                    else {"with_item_data": True}
                )

                objects = [
                    obj.to_dict(**obj_kws)
                    for obj in query.limit(limit).all()
                ]

                if objects:
                    resp[resp_key] = objects

        return resp, 200

    def _handle_normal_search(self, search_string: str, limit: int = 15):
        items = (
            ItemList.query
            .filter(or_(
                ItemList.name.contains(search_string),
                ItemList.code.contains(search_string),
            )).limit(
                limit
            ).all()
        )

        monsters = (
            Monster.query
            .filter(or_(
                Monster.name.contains(search_string),
                Monster.code.contains(search_string),
            )).limit(
                limit
            ).all()
        )

        npcs = (
            Npc.query.filter(or_(
                Npc.name.contains(search_string),
                Npc.code.contains(search_string),
            )).limit(
                limit
            ).all()
        )

        quests = (
            Quest.query.filter(or_(
                Quest.title.contains(search_string),
                Quest.code.contains(search_string),
            )).limit(
                limit
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
                limit
            ).all()
        )

        players = (
            RankingPlayer.query
            .filter(
                RankingPlayer.name.contains(search_string)
            ).order_by(
                RankingPlayer.rank,
            ).limit(
                limit
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
