import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.core.enums import QuestMissionType
from src.database.base import Base
from src.updater import strategies
from src.updater.schema import LoaderInfo


class QuestGiveItem(Base):
    __table_args__ = (sa.PrimaryKeyConstraint("quest_code", "item_code"),)

    quest_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("quest.code"),
        nullable=False,
    )
    item_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("item_list.code"),
        index=True,
        nullable=False,
    )
    item = orm.relationship(
        "ItemList",
        foreign_keys=[item_code],
        uselist=False,
        viewonly=True,
    )
    amount = orm.mapped_column(
        sa.Integer,
        nullable=False,
    )


class QuestRewardItem(Base):
    # Apparently there are quests that reward the same item, fuck that
    # __table_args__ = (sa.PrimaryKeyConstraint("quest_code", "item_code"),)

    index = orm.mapped_column(
        sa.Integer,
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )
    quest_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("quest.code"),
        nullable=False,
    )
    item_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("item_list.code"),
        index=True,
        nullable=False,
    )
    item = orm.relationship(
        "ItemList",
        foreign_keys=[item_code],
        uselist=False,
        viewonly=True,
    )
    amount = orm.mapped_column(
        sa.Integer,
        nullable=False,
    )


class QuestMission(Base):
    index = orm.mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
    )

    quest_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("quest.code"),
        nullable=False,
    )
    work_type = orm.mapped_column(
        sa.Enum(QuestMissionType),
        nullable=False,
    )
    count = orm.mapped_column(
        sa.Integer,
        nullable=False,
    )
    description = orm.mapped_column(
        sa.Text,
        nullable=False,
    )

    map_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("map.code"),
        nullable=True,
    )
    map = orm.relationship(
        "Map",
        foreign_keys=[map_code],
    )
    x = orm.mapped_column(
        sa.Float,
        nullable=True,
    )
    y = orm.mapped_column(
        sa.Float,
        nullable=True,
    )

    monster_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("monster.code"),
        nullable=True,
    )
    monster = orm.relationship(
        "Monster",
        foreign_keys=[monster_code],
    )

    item_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("item_list.code"),
        index=True,
        nullable=True,
    )
    item = orm.relationship(
        "ItemList",
        foreign_keys=[item_code],
        uselist=False,
        viewonly=True,
    )

    quest_item_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("quest_item.code"),
        nullable=True,
    )
    quest_item = orm.relationship(
        "QuestItem",
        foreign_keys=[quest_item_code],
    )

    npc_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("npc.code"),
        nullable=True,
    )
    npc = orm.relationship(
        "Npc",
        foreign_keys=[npc_code],
    )


class Quest(Base):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(extra_files=["QuestIndex.xml", "StringData_EN.in_"]),
        loader_strategy=strategies.quest,
    )

    code = orm.mapped_column(
        sa.String(32),
        primary_key=True,
    )
    is_sea = orm.mapped_column(
        sa.Boolean,
        nullable=False,
    )
    level = orm.mapped_column(
        sa.Integer,
        nullable=False,
    )

    is_mercenary = orm.mapped_column(
        sa.Boolean,
        nullable=False,
    )
    is_saint = orm.mapped_column(
        sa.Boolean,
        nullable=False,
    )
    is_noble = orm.mapped_column(
        sa.Boolean,
        nullable=False,
    )
    is_explorer = orm.mapped_column(
        sa.Boolean,
        nullable=False,
    )

    experience = orm.mapped_column(
        sa.Integer,
        nullable=False,
    )
    money = orm.mapped_column(
        sa.Integer,
        nullable=False,
    )
    selectable_items_count = orm.mapped_column(
        sa.Integer,
        nullable=False,
    )

    title = orm.mapped_column(
        sa.Text,
        nullable=False,
    )
    description = orm.mapped_column(
        sa.Text,
        nullable=True,
    )
    pre_dialog = orm.mapped_column(
        sa.Text,
        nullable=True,
    )
    start_dialog = orm.mapped_column(
        sa.Text,
        nullable=True,
    )
    run_dialog = orm.mapped_column(
        sa.Text,
        nullable=True,
    )
    finish_dialog = orm.mapped_column(
        sa.Text,
        nullable=True,
    )

    previous_quest_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("quest.code"),
        nullable=True,
    )

    previous_quest = orm.relationship(
        "Quest",
        uselist=False,
        viewonly=True,
        primaryjoin="foreign(Quest.code) == Quest.previous_quest_code",
    )

    start_npc_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("npc.code"),
        nullable=True,
    )
    start_npc = orm.relationship(
        "Npc",
        uselist=False,
        viewonly=True,
        foreign_keys=[start_npc_code],
    )

    # Some unused quests (which are later filtered out) appear to not have a
    # starting area, so we set the field here to nullable (and therefore the relationship)
    # despite it *supposedly* always having a map/area.
    start_area_code = orm.mapped_column(
        sa.String(32),
        nullable=True,
    )
    start_area = orm.relationship(
        "MapArea",
        primaryjoin="or_(foreign(MapArea.map_code) == Quest.start_area_code, foreign(MapArea.area_code) == Quest.start_area_code)",
        uselist=False,
        viewonly=True,
    )

    end_npc_code = orm.mapped_column(
        sa.String(32),
        sa.ForeignKey("npc.code"),
        nullable=True,
    )
    end_npc = orm.relationship(
        "Npc",
        uselist=False,
        viewonly=True,
        foreign_keys=[end_npc_code],
    )

    give_items = orm.relationship(
        "QuestGiveItem",
        uselist=True,
        viewonly=True,
    )
    reward_items = orm.relationship(
        "QuestRewardItem",
        uselist=True,
        viewonly=True,
    )
    missions = orm.relationship(
        "QuestMission",
        uselist=True,
        viewonly=True,
    )
