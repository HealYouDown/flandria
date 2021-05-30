from webapp.extensions import db
from webapp.models.enums import Area, QuestWorkType


class QuestDescription(db.Model):
    __tablename__ = "quest_description"

    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    language = db.Column(db.String(4), nullable=False)

    quest_code = db.Column(db.String(32), db.ForeignKey("quest.code"))

    title = db.Column(db.Text(256))

    mission_1 = db.Column(db.Text(1024))
    mission_2 = db.Column(db.Text(1024))
    mission_3 = db.Column(db.Text(1024))

    description = db.Column(db.Text(2048))

    pre_dialog = db.Column(db.Text(2048))
    start_dialog = db.Column(db.Text(2048))
    run_dialog = db.Column(db.Text(2048))
    finish_dialog = db.Column(db.Text(2048))

    def to_dict(self) -> dict:
        return {
            "language": self.language,
            "title": self.title,
            "missions": [
                self.mission_1,
                self.mission_2,
                self.mission_3,
            ],
            "description": self.description,
            "pre_dialog": self.pre_dialog,
            "run_dialog": self.run_dialog,
            "start_dialog": self.start_dialog,
            "finish_dialog": self.finish_dialog,
        }


class QuestGiveItem(db.Model):
    __tablename__ = "quest_give_item"

    index = db.Column(db.Integer, primary_key=True, autoincrement=True)

    quest_code = db.Column(db.String(32), db.ForeignKey("quest.code"),
                           nullable=False)
    quest = db.relationship("Quest", foreign_keys=[quest_code],
                            viewonly=True,)

    item_code = db.Column(db.String(32), db.ForeignKey("item_list.code"),
                          nullable=False)
    item = db.relationship("ItemList", foreign_keys=[item_code],
                           uselist=False, viewonly=True,)

    amount = db.Column(db.Integer, nullable=False)

    def to_dict(self) -> dict:
        return {
            "item": self.item.to_dict(),
            "amount": self.amount,
        }


class QuestSelectableItem(db.Model):
    __tablename__ = "quest_selectable_item"

    index = db.Column(db.Integer, primary_key=True, autoincrement=True)

    quest_code = db.Column(db.String(32), db.ForeignKey("quest.code"),
                           nullable=False)
    quest = db.relationship("Quest", foreign_keys=[quest_code],
                            viewonly=True,)

    item_code = db.Column(db.String(32), db.ForeignKey("item_list.code"),
                          nullable=False)
    item = db.relationship("ItemList", foreign_keys=[item_code],
                           uselist=False, viewonly=True,)

    amount = db.Column(db.Integer, nullable=False)

    def to_dict(self) -> dict:
        return {
            "item": self.item.to_dict(),
            "amount": self.amount,
        }


class QuestMission(db.Model):
    __tablename__ = "quest_mission"

    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    work_type = db.Column(db.Enum(QuestWorkType), nullable=False)
    work_value = db.Column(db.String(32))

    quest_code = db.Column(db.String(32), db.ForeignKey("quest.code"),
                           nullable=False)

    quest = db.relationship("Quest", foreign_keys=[quest_code],
                            viewonly=True,)

    map_code = db.Column(db.String(32), db.ForeignKey("map.code"))
    map = db.relationship("Map", foreign_keys=[map_code],
                          uselist=False, viewonly=True,)

    x = db.Column(db.Float)
    y = db.Column(db.Float)

    count = db.Column(db.Integer, nullable=False)

    npc_code = db.Column(db.String(32), db.ForeignKey("npc.code"))
    npc = db.relationship("Npc", foreign_keys=[npc_code],
                          uselist=False, viewonly=True,)

    item_code = db.Column(db.String(32), db.ForeignKey("item_list.code"))
    item = db.relationship("ItemList", foreign_keys=[item_code],
                           uselist=False, viewonly=True,)

    monster_code = db.Column(db.String(32), db.ForeignKey("monster.code"))
    monster = db.relationship("Monster", foreign_keys=[monster_code],
                              uselist=False, viewonly=True,)

    quest_item_code = db.Column(db.String(32),
                                db.ForeignKey("quest_item.code"))
    quest_item = db.relationship("QuestItem", foreign_keys=[quest_item_code],
                                 uselist=False, viewonly=True,)

    def to_dict(self) -> dict:
        return {
            "work_type": self.work_type.to_dict(),
            "work_value": self.work_value,
            "map": (self.map.to_dict(minimal=True)
                    if self.map else None),
            "pos": {
                "x": self.x,
                "y": self.y,
            },
            "count": self.count,
            "npc": self.npc.to_dict(minimal=True) if self.npc else None,
            "item": self.item.to_dict() if self.item else None,
            "monster": (self.monster.to_dict(minimal=True)
                        if self.monster else None),
            "quest_item": (self.quest_item.to_dict(minimal=True)
                           if self.quest_item else None)
        }


class Quest(db.Model):
    __tablename__ = "quest"

    index = db.Column(db.Integer, nullable=False)
    code = db.Column(db.String(32), primary_key=True, nullable=False)

    level = db.Column(db.Integer, nullable=False)
    area = db.Column(db.Enum(Area), nullable=False)
    class_ = db.Column(db.String(16))
    money = db.Column(db.Integer)
    experience = db.Column(db.Integer)
    title = db.Column(db.String(256), nullable=False, index=True)

    selectable_items_count = db.Column(db.Integer)

    before_quest_code = db.Column(db.String(32))
    before_quest = db.relationship(
        "Quest",
        primaryjoin="foreign(Quest.code) == Quest.before_quest_code",
        uselist=False, viewonly=True,)

    after_quest = db.relationship(
        "Quest",
        primaryjoin="foreign(Quest.before_quest_code) == Quest.code",
        uselist=False, viewonly=True,)

    start_npc_code = db.Column(db.String(32), db.ForeignKey("npc.code"))
    start_npc = db.relationship("Npc", foreign_keys=[start_npc_code],
                                uselist=False, viewonly=True,)

    end_npc_code = db.Column(db.String(32), db.ForeignKey("npc.code"))
    end_npc = db.relationship("Npc", foreign_keys=[end_npc_code],
                              uselist=False, viewonly=True,)

    start_area_code = db.Column(db.String(32), db.ForeignKey("map.code"))
    start_area = db.relationship("Map", foreign_keys=[start_area_code],
                                 viewonly=True,)

    missions = db.relationship("QuestMission", viewonly=True)
    selectable_items = db.relationship("QuestSelectableItem", viewonly=True)
    give_items = db.relationship("QuestGiveItem", viewonly=True)
    descriptions = db.relationship(
        "QuestDescription",
        primaryjoin="foreign(QuestDescription.quest_code) == Quest.code",
        viewonly=True,
    )

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = {
            "code": self.code,
            "area": self.area.to_dict(),
            "class": self.class_,
            "level": self.level,
            "title": self.title,
        }

        if minimal:
            return minimal_dict

        return {
            **minimal_dict,
            "money": self.money,
            "experience": self.experience,
            "selectable_items_count": self.selectable_items_count,
            "start_npc": (self.start_npc.to_dict(minimal=True)
                          if self.start_npc else None),
            "end_npc": (self.end_npc.to_dict(minimal=True)
                        if self.end_npc else None),
            "start_area": (self.start_area.to_dict(minimal=True)
                           if self.start_area else None),
            "before_quest": (self.before_quest.to_dict(minimal=True)
                             if self.before_quest else None),
            "after_quest": (self.after_quest.to_dict(minimal=True)
                            if self.after_quest else None),
            "missions": [mission.to_dict() for mission in self.missions],
            "give_items": [gitem.to_dict() for gitem in self.give_items],
            "selectable_items": [sitem.to_dict()
                                 for sitem in self.selectable_items],
            "descriptions": {
                desc.language: desc.to_dict()
                for desc in self.descriptions
            },
        }
