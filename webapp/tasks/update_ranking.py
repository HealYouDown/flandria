import collections
import enum
import io
import json
import multiprocessing
import os
import sys
import time
import typing

import requests
from flask import current_app
from lxml import html
from webapp.extensions import db
from webapp.models import RankingPlayer, RankingPlayerHistory
from webapp.models.enums import CharacterClass, Server

RANKING_URL = "https://www.florensia-online.com/de/rankings?page={page}"


class JSONEncoderWithEnumSupport(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, enum.Enum):
            return obj.to_dict()

        return json.JSONEncoder.default(self, obj)


def get_max_page() -> int:
    """Scraps the first page to find out how many pages there are.

    Returns:
        int: The maximum page number.
    """
    # Get the maximum pages
    with requests.get(RANKING_URL.format(page=1)) as req:
        parser = html.parse(io.BytesIO(req.content))
        pagination_numbers = parser.xpath(
            "//li[starts-with(@class, 'page-item')]/*/text()")
        # Pagination numbers will look like:
        # ['«', '1', '2', '3', '4', '3532', '3533', '»']

        return int(pagination_numbers[-2])


def scrap_page(
    page: int
) -> typing.Union[
    typing.List[dict],
    int
]:
    """Scraps a given page.

    Args:
        page (int): The number of the page

    Returns:
        typing.Union[ typing.List[dict], int ]: Either a list with up to
            50 players dict or the status code, if it was not 200.
    """
    url = RANKING_URL.format(page=page)

    with requests.get(url) as req:
        if req.status_code != 200:
            return req.status_code

        parser = html.parse(io.BytesIO(req.content))

        table_data_elements = parser.xpath("//tbody/tr/td")
        table_data = [elem.text for elem in table_data_elements]

    # Each player consists of 10 items in table data
    # e.g. ['4', None, 'Fufu', 'Magic Knight', '105', None, '99', None,
    # '¤CryClown¤', 'LuxPlena']
    player_count = len(table_data) // 10

    players = []
    for i in range(player_count):
        player_data = table_data[i*10:i*10 + 10]

        server = (Server.bergruen
                  if player_data[9] == "Bergruen"
                  else Server.luxplena)

        character_class = CharacterClass.from_name(player_data[3])

        players.append({
            "composite_key_string": f"{server.name}_{player_data[2]}",
            "rank": int(player_data[0]),
            "name": player_data[2],
            "character_class": character_class,
            "level_land": int(player_data[4]),
            "level_sea": int(player_data[6]),
            "guild": player_data[8],
            "server": server,
        })

    return players


def get_players() -> None:
    """Scraps the official florensia ranking."""
    process_count = int(os.getenv("RANKING_PROCESS_COUNT", 4))
    max_page = get_max_page()
    page_nums = range(1, max_page+1)

    players = []
    with multiprocessing.Pool(processes=process_count) as pool:
        for index, result in enumerate(pool.imap(scrap_page, page_nums)):
            page = index + 1

            if isinstance(result, list):
                players.extend(result)

            elif isinstance(result, int):
                # An error occured, result is status code
                current_app.logger.warning(
                    f"Failed to scrap page {page} - {result}")

            # Log process each xx pages or when finished
            if page % 100 == 0 or page == max_page:
                current_app.logger.info(
                    f"Scrapped {page}/{max_page} pages.")

    return players


def save_ranking(data: list) -> None:
    with open("ranking.json", "w") as fp:
        json.dump(
            data, fp, indent=2,
            cls=JSONEncoderWithEnumSupport,
            ensure_ascii=True)


def update_ranking():
    # Scrap all players
    t1 = time.time()
    players = get_players()
    # save_ranking(players)
    t2 = time.time()

    current_app.logger.info(
        f"Finished scrapping - took {round(t2 - t1, 2)}s")

    # Loading players from local json file
    """
    players = []
    with open("ranking.json", "r") as fp:
        for player in json.load(fp):
            player["character_class"] = (
                CharacterClass(player["character_class"]["value"]))
            player["server"] = Server(player["server"]["value"])
            players.append(player)
    """

    # Now update, delete or insert players, based on the data from
    # the ranking
    t1 = time.time()

    # Get all ids that are in the database and should be updated
    keys = [player["composite_key_string"] for player in players]

    # Filter out duplicate people on the same server
    # As of now (08.01.2021), this is just one player: "KUM", who
    # exists two times on LuxPlena. I don't deal with that shit.
    # Just remove both from the whole ranking.
    counter = collections.Counter(keys)
    exclude_player_keys = []
    for key, count in counter.items():
        if count > 1:
            current_app.logger.warning(f"Removed duplicate player {key}")
            exclude_player_keys.append(key)

    players = [player for player in players
               if player["composite_key_string"] not in exclude_player_keys]

    # keys contains all players that were found in the ranking. If a player
    # does not exist anymore, its key won't be in there, so delete the player
    players_in_database: typing.List[RankingPlayer] = []

    # Database is queried in chunks as there is a limit with how many variables
    # can be in the in_ clause.
    chunksize = 20000

    for i in range(0, len(keys), chunksize):
        # First, add all players that are in the database and still
        # in the ranking data
        players_in_database.extend(
            RankingPlayer.query
            .filter(
                RankingPlayer.composite_key_string.in_(
                    keys[i:i+chunksize]
                )
            ).all()
        )

    # Get composite keys from ALL users in database, ignoring if they exist in
    # the ranking data or not
    all_composite_keys = [
        row.composite_key_string for row in
        RankingPlayer.query.with_entities(
            RankingPlayer.composite_key_string
        ).all()
    ]

    # To find out which players exist in database but no longer in ranking,
    # compare composite keys
    diff_keys = list(set(all_composite_keys).difference(keys))
    deleted_players_count = len(diff_keys)

    # Failsafe.
    # If for some reasons ranking is buggy and script tries to delete *a lot*
    # of players stop it from doing so and log an error.
    # I doubt that there will be more than 5000 deleted users a single day
    # (hope so?)
    if deleted_players_count >= 5000:
        current_app.logger.error(
            f"Tried to delete {deleted_players_count} players.")
        sys.exit(1)

    # just in case that more than ~32k players in one night are deleted, we
    # delete players in chunks
    for i in range(0, len(diff_keys), chunksize):
        # Delete ranking players
        query = (
            RankingPlayer.query
            .filter(
                RankingPlayer.composite_key_string.in_(
                    diff_keys[i:i+chunksize]
                )
            )
        )

        # Delete history
        # (Cascade on the player object does not work)
        players_to_delete = query.all()
        for player in players_to_delete:
            for history in player.history:
                db.session.delete(history)

        # execute delete statement on player rows
        query.delete(synchronize_session="fetch")

    # Dict that has the composite key as key and the player object
    # as the value
    players_in_database_dict = {
        player.composite_key_string: player
        for player in players_in_database
    }
    player_composite_keys = players_in_database_dict.keys()

    players_to_update = []
    players_to_insert = []
    players_history = []

    for player in players:
        if player["composite_key_string"] in player_composite_keys:
            # Check if user did change in any way and add it to the history
            compare_columns = ["level_land", "level_sea", "character_class",
                               "guild"]
            player_obj = (
                players_in_database_dict[player["composite_key_string"]])

            history = {}

            # Compare different columns and only add changed values
            for column in compare_columns:
                if player[column] != getattr(player_obj, column):
                    history[f"previous_{column}"] = getattr(player_obj, column)
                    history[f"new_{column}"] = player[column]

            if history:
                # add name and server if columns changed,
                # those are used to link to the main player
                # object
                history["name"] = player["name"]
                history["server"] = player["server"]

                players_history.append(history)
                players_to_update.append(player)

        else:
            players_to_insert.append(player)

    current_app.logger.info(f"Deleting {deleted_players_count} players.")
    current_app.logger.info(f"Updating {len(players_to_update)} players.")
    current_app.logger.info(f"Adding {len(players_to_insert)} new players.")

    if players_to_update:
        db.session.bulk_update_mappings(RankingPlayer, players_to_update)

    if players_to_insert:
        db.session.bulk_insert_mappings(RankingPlayer, players_to_insert)

    if players_history:
        db.session.bulk_insert_mappings(RankingPlayerHistory, players_history)

    db.session.commit()

    t2 = time.time()

    current_app.logger.info(
        f"Finish updating ranking - took {round(t2 - t1, 2)}s"
    )
