from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, relation
from ...extensions import db


class QuestMission(db.Model):
    __tablename__ = "quest_mission"
    __bind_key__ = "static_data"

    index = Column(Integer, primary_key=True, autoincrement=True)
    quest_code = Column(String, ForeignKey('quest.code'))

    work_type = Column(Integer)
    work_value = Column(String)
    count = Column(Integer)

    # 0
    item_code = Column(String, ForeignKey("item_list.code"))
    item = relationship("ItemList", foreign_keys=[item_code])

    # 1, 4, 17
    npc_code = Column(String, ForeignKey("npc.code"))
    npc = relationship("NPC", foreign_keys=[npc_code])

    # 2
    monster_code = Column(String, ForeignKey("monster.code"))
    monster = relationship("Monster", foreign_keys=[monster_code])

    # 3
    quest_item_code = Column(String, ForeignKey("quest_item.code"))
    quest_item = relationship("QuestItem", foreign_keys=[quest_item_code])

    def to_dict(self) -> dict:
        d = {
            "work_type": self.work_type,
            "work_value": self.work_value,
            "count": self.count,
        }

        if self.work_type in [0]:
            d["item"] = self.item.to_dict()

        elif self.work_type in [1, 4, 17]:
            d["npc"] = self.npc.to_dict()

        elif self.work_type == 2:
            d["monster"] = self.monster.to_dict(minimal=True)

        elif self.work_type == 3:
            d["quest_item"] = self.quest_item.to_dict(minimal=True)

        return d


class QuestGiveDescription(db.Model):
    __tablename__ = "quest_give_description"
    __bind_key__ = "static_data"

    index = Column(Integer, primary_key=True, autoincrement=True)
    quest_code = Column(String, ForeignKey('quest.code'))

    item_code = Column(String, ForeignKey("quest_item.code"))
    item = relationship("QuestItem", foreign_keys=[item_code])

    amount = Column(Integer)

    def to_dict(self) -> dict:
        return {
            "amount": self.amount,
            "item": None if self.item is None else self.item.to_dict()
        }


class QuestLootDescription(db.Model):
    __tablename__ = "quest_loot_description"
    __bind_key__ = "static_data"

    index = Column(Integer, primary_key=True, autoincrement=True)
    quest_code = Column(String, ForeignKey('quest.code'))

    monster_code = Column(String, ForeignKey("monster.code"))
    monster = relationship("Monster", foreign_keys=[monster_code])

    item_code = Column(String, ForeignKey("quest_item.code"))
    item = relationship("QuestItem", foreign_keys=[item_code])

    rate = Column(Integer)

    def to_dict(self) -> dict:
        return {
            "item": self.item.to_dict(minimal=True),
            "rate": self.rate,
        }


class QuestSelectableItem(db.Model):
    __tablename__ = "quest_selectable_item"
    __bind_key__ = "static_data"

    index = Column(Integer, primary_key=True, autoincrement=True)
    quest_code = Column(String, ForeignKey('quest.code'))

    item_code = Column(String, ForeignKey("item_list.code"))
    item = relationship("ItemList", foreign_keys=[item_code])

    amount = Column(Integer)

    def to_dict(self) -> dict:
        return {
            "item": self.item.to_dict(),
            "amount": self.amount,
        }


class QuestDescription(db.Model):
    __tablename__ = "quest_description"
    __bind_key__ = "static_data"

    index = Column(Integer, primary_key=True, autoincrement=True)

    quest_code = Column(String, ForeignKey("quest.code"))
    language_code = Column(String)

    title = Column(String)
    mission_1 = Column(String)
    mission_2 = Column(String)
    mission_3 = Column(String)
    desc = Column(String)
    pre_dialog = Column(String)
    start_dialog = Column(String)
    run_dialog = Column(String)
    finish_dialog = Column(String)

    def to_dict(self) -> dict:
        return {
            "language_code": self.language_code,
            "title": self.title,
            "mission_1": self.mission_1,
            "mission_2": self.mission_2,
            "mission_3": self.mission_3,
            "description": self.desc,
            "pre_dialog": self.pre_dialog,
            "start_dialog": self.start_dialog,
            "run_dialog": self.run_dialog,
            "finish_dialog": self.finish_dialog
        }


class Quest(db.Model):
    __tablename__ = "quest"
    __bind_key__ = "static_data"

    index = Column(Integer)

    code = Column(String, primary_key=True)
    name = Column(String)
    level = Column(Integer)
    player_class = Column(String)
    exp_reward = Column(Integer)
    money_reward = Column(Integer)
    location = Column(Integer)

    before_quest_code = Column(String, ForeignKey("quest.code"))
    before_quest = relation("Quest", remote_side=[code])

    source_object_code = Column(String, ForeignKey("npc.code"))
    source_object = relationship("NPC", foreign_keys=[source_object_code])

    source_area_code = Column(String, ForeignKey("map.code"))
    source_area = relationship("Map", foreign_keys=[source_area_code])

    supplier_code = Column(String, ForeignKey("npc.code"))
    supplier = relationship("NPC", foreign_keys=[supplier_code])

    give_descriptions = relationship("QuestGiveDescription")
    loot_descriptions = relationship("QuestLootDescription")
    selectable_items = relationship("QuestSelectableItem")
    missions = relationship("QuestMission")
    descriptions = relationship("QuestDescription")

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = {
            "code": self.code,
            "name": self.name,
            "location": self.location,
            "level": self.level,
        }

        if minimal:
            return minimal_dict

        d = {
            **minimal_dict,
            "player_class": self.player_class,
            "exp_reward": self.exp_reward,
            "money_reward": self.money_reward,
            "start_map": self.source_area.to_dict(),
        }

        # Before Quest
        if self.before_quest_code is not None:
            d["before_quest"] = self.before_quest.to_dict(minimal=True)
        else:
            d["before_quest"] = None

        # Start NPC
        if self.source_object is not None:
            d["start_npc"] = self.source_object.to_dict()
        else:
            d["start_npc"] = None

        # Finish NPC
        if self.supplier is not None:
            d["finish_npc"] = self.supplier.to_dict()
        else:
            d["finish_npc"] = None

        # Given Quest items
        d["given_quest_items"] = [obj.to_dict() for
                                  obj in self.give_descriptions]

        # Needed quest items to collect
        d["needed_quest_items"] = [obj.to_dict() for
                                   obj in self.loot_descriptions]

        # Rewards
        d["rewards"] = [obj.to_dict() for
                        obj in self.selectable_items]

        # Missions
        d["missions"] = [obj.to_dict() for
                         obj in self.missions]

        # Description
        d["descriptions"] = {
            obj.language_code: obj.to_dict()
            for obj in self.descriptions
        }

        return d
