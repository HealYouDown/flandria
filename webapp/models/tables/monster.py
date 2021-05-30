from webapp.extensions import db
from webapp.models.custom_sql_classes import CustomColumn
from webapp.models.enums import Area, MonsterRange, RatingType
from webapp.models.transforms import (florensia_meter_transform,
                                      florensia_probability_transform)


class Monster(db.Model):
    __tablename__ = "monster"

    _mapper_utils = {
        "files": {
            "server": [
                "s_MonsterChar.bin"
            ],
            "client": [
                "c_MonsterCharRes.bin"
            ],
            "string": [
                "MonsterCharStr.dat"
            ],
        },
        "options": {
            "image_key": "모델명"
        },
    }

    index = db.Column(db.Integer, nullable=False)

    code = CustomColumn(db.String(32),
                        primary_key=True,
                        mapper_key="코드")

    name = CustomColumn(db.String(256),
                        nullable=False,
                        mapper_key="_name",
                        index=True)

    icon = CustomColumn(db.String(32),
                        nullable=False,
                        mapper_key="_icon")

    rating_type = CustomColumn(db.Enum(RatingType),
                               nullable=False,
                               mapper_key="몬스터등급타입",
                               transform=lambda val: RatingType(val))

    level = CustomColumn(db.Integer,
                         nullable=False,
                         mapper_key="기준레벨")

    hp = CustomColumn(db.Integer,
                      nullable=False,
                      mapper_key="기준최대HP")

    range = CustomColumn(db.Enum(MonsterRange),
                         nullable=False,
                         mapper_key="공격거리타입",
                         transform=lambda val: MonsterRange(val))

    area = CustomColumn(db.Enum(Area),
                        nullable=False,
                        mapper_key="필드구분",
                        transform=lambda val: Area(val))

    experience = CustomColumn(db.Integer,
                              nullable=False,
                              mapper_key="보상경험치")

    minimal_damage = CustomColumn(db.Integer,
                                  nullable=False,
                                  mapper_key="최소물공력")

    maximal_damage = CustomColumn(db.Integer,
                                  nullable=False,
                                  mapper_key="최대물공력")

    physical_defense = CustomColumn(db.Integer,
                                    nullable=False,
                                    mapper_key="물방력")

    magic_defense = CustomColumn(db.Integer,
                                 nullable=False,
                                 mapper_key="마항력")

    attack_range = CustomColumn(db.Float,
                                nullable=False,
                                mapper_key="기본사정거리",
                                transform=florensia_meter_transform)

    tameable = CustomColumn(db.Boolean,
                            mapper_key="테이밍",
                            nullable=False)

    drops = db.relationship(
        "Drop",
        primaryjoin="foreign(Drop.monster_code) == Monster.code",
        viewonly=True,)

    map_points = db.relationship(
        "MapPoint",
        primaryjoin="foreign(MapPoint.monster_code) == Monster.code",
        viewonly=True,
    )

    quest_missions = db.relationship(
        "QuestMission",
        primaryjoin="foreign(QuestMission.monster_code) == Monster.code",
        viewonly=True,
    )

    vision_range = CustomColumn(db.Float,
                                nullable=False,
                                mapper_key="선공시야",
                                transform=florensia_meter_transform)

    # If you perform an action close to the range
    # attack vision range of the monster, you will
    # also get aggro
    attack_vision_range = CustomColumn(
        db.Float, nullable=False, mapper_key="요청시야",
        transform=florensia_meter_transform)

    messages_code = CustomColumn(
        db.String(32), mapper_key="오브젝트채팅",
        transform=lambda v: v if v != "#" else None)

    monster_message = db.relationship(
        "MonsterMessage",
        primaryjoin="foreign(MonsterMessage.code) == Monster.messages_code",
        uselist=False,
        viewonly=True)

    # Skill 1
    skill_1_code = CustomColumn(
        db.String(32), db.ForeignKey("monster_skill.code"),
        mapper_key="부가Action1코드",
        transform=lambda v: v if v != "#" else None)

    skill_1_chance = CustomColumn(
        db.Float, mapper_key="부가Action1선택율",
        transform=florensia_probability_transform)

    skill_1 = db.relationship("MonsterSkill", foreign_keys=[skill_1_code],
                              viewonly=True,)

    # Skill 2
    skill_2_code = CustomColumn(
        db.String(32), db.ForeignKey("monster_skill.code"),
        mapper_key="부가Action2코드",
        transform=lambda v: v if v != "#" else None)

    skill_2_chance = CustomColumn(
        db.Float, mapper_key="부가Action2선택율",
        transform=florensia_probability_transform)

    skill_2 = db.relationship("MonsterSkill", foreign_keys=[skill_2_code],
                              viewonly=True,)

    def to_dict(self, minimal: bool = False) -> dict:
        minimal_dict = {
            "code": self.code,
            "name": self.name,
            "icon": self.icon,
            "rating": self.rating_type.to_dict(),
            "level": self.level,
            "area": self.area.to_dict(),
        }

        if minimal:
            return minimal_dict

        # Get monster skills as a list
        skills = []
        for i in range(1, 3):
            skill = getattr(self, f"skill_{i}")
            if skill:
                skill_dict = skill.to_dict()
                skill_dict["chance"] = getattr(self, f"skill_{i}_chance")
                skills.append(skill_dict)

        return {
            **minimal_dict,
            "hp": self.hp,
            "range": self.range.to_dict(),
            "experience": self.experience,
            "minimal_damage": self.minimal_damage,
            "maximal_damage": self.maximal_damage,
            "physical_defense": self.physical_defense,
            "magic_defense": self.magic_defense,
            "attack_range": self.attack_range,
            "tamable": self.tameable,
            "vision_range": self.vision_range,
            "attack_vision_range": self.attack_vision_range,
            "messages": (self.monster_message.to_dict()
                         if self.monster_message
                         else None),
            "skills": skills,
            "map_points": [point.to_dict(map_dict=True)
                           for point in self.map_points],
            "drops": [drop.to_dict(item_dict=True) for drop in self.drops],
            "quests": [mission.quest.to_dict(minimal=True)
                       for mission in self.quest_missions]
        }
