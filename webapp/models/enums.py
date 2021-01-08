import enum

"""
These Enums all map the different values that florensia uses
in their files.
"""


class Server(enum.Enum):
    luxplena = 0
    bergruen = 1

    @property
    def names(self) -> dict:
        return {
            Server.luxplena: "LuxPlena",
            Server.bergruen: "Bergruen",
        }

    def to_dict(self) -> dict:
        return {
            "value": self.value,
            "name": self.names.get(self),
        }


class EssenceEquipType(enum.Enum):
    all = 0
    weapons = 1
    armor = 2
    shield = 3
    dress = 4
    dress_amor_shield = 5
    dress_armor = 6
    weapons_armor = 7
    dress_weapons_armor = 8
    weapons_shield = 9

    @property
    def names(self) -> dict:
        return {
            EssenceEquipType.all: "All",
            EssenceEquipType.weapons: "Weapons",
            EssenceEquipType.armor: "Armor",
            EssenceEquipType.shield: "Shield",
            EssenceEquipType.dress: "Dress",
            EssenceEquipType.dress_amor_shield: "Dress, Armor, Shield",
            EssenceEquipType.dress_armor: "Dress, Armor",
            EssenceEquipType.weapons_armor: "Weapons, Armor",
            EssenceEquipType.dress_weapons_armor: "Dress, Weapons, Armor",
            EssenceEquipType.weapons_shield: "Weapons, Shield",
        }

    def to_dict(self) -> dict:
        return {
            "value": self.value,
            "name": self.names.get(self),
        }


class RatingType(enum.Enum):
    """Enum that contains the different rating types
    for monsters."""
    normal = 0
    elite_monster = 1
    mini_boss = 2
    boss = 3

    @property
    def names(self) -> dict:
        return {
            RatingType.normal: "Normal",
            RatingType.elite_monster: "Elite",
            RatingType.mini_boss: "Mini-Boss",
            RatingType.boss: "Boss",
        }

    def to_dict(self) -> dict:
        return {
            "value": self.value,
            "name": self.names.get(self)
        }


class Area(enum.Enum):
    """Enum that contains the different areas for monsters
    and quests: Land and Sea"""
    land = 0
    sea = 1

    @property
    def names(self) -> dict:
        return {
            Area.land: "Land",
            Area.sea: "Sea",
        }

    def to_dict(self) -> dict:
        return {
            "value": self.value,
            "name": self.names.get(self)
        }


class MonsterRange(enum.Enum):
    """Enum that contains the different ranges for monsters,
    they can be either melee or range."""
    melee = 0
    range = 1

    @property
    def names(self) -> dict:
        return {
            MonsterRange.melee: "Melee",
            MonsterRange.range: "Range",
        }

    def to_dict(self) -> dict:
        return {
            "value": self.value,
            "name": self.names.get(self),
        }


class QuestWorkType(enum.Enum):
    # 6, 7, 8 and 18 are excluded
    deliver_item = 0
    talk_to_npc = 1
    kill_monster = 2
    collect_quest_item = 3
    convoy_npc = 4
    equip_item = 5
    # unknown_1 = 6
    # unknown_2 = 7
    # unknown_3 = 8
    use_skillbook = 9
    use_skillpoint = 10
    add_consumable_to_slot_bar = 11
    add_skill_to_slot_bar = 12
    register_ship = 13
    tune_ship = 14
    equip_sea_shells = 15
    change_weapons = 16
    listen_to_npc = 17  # Same as 1?
    # unknown_4 = 18

    @property
    def names(self) -> dict:
        return {}

    def to_dict(self) -> dict:
        return {
            "value": self.value,
            "name": self.names.get(self, None),
        }


class Gender(enum.Enum):
    male = 0
    female = 1
    both = 4294967295

    @property
    def names(self) -> dict:
        return {
            Gender.male: "Male",
            Gender.female: "Female",
            Gender.both: "Male, Female",
        }

    def to_dict(self) -> dict:
        return {
            "value": self.value,
            "name": self.names.get(self)
        }


class AccessoryType(enum.Enum):
    necklace = 0
    earring = 1
    ring = 2

    @property
    def names(self) -> dict:
        return {
            AccessoryType.necklace: "Necklace",
            AccessoryType.earring: "Earring",
            AccessoryType.ring: "Ring",
        }

    def to_dict(self) -> dict:
        return {
            "value": self.value,
            "name": self.names.get(self)
        }


class WeaponType(enum.Enum):
    duals = "P"
    rifle = "R"
    cariad = "C"
    shield = "B"
    rapier = "A"
    two_handed_sword = "T"
    one_handed_sword = "S"
    dagger = "D"
    fishing_rod = "F"
    all = "X"

    @property
    def names(self) -> dict:
        return {
            WeaponType.duals: "Duals",
            WeaponType.rifle: "Rifle",
            WeaponType.cariad: "Cariad",
            WeaponType.shield: "Shield",
            WeaponType.two_handed_sword: "Two-handed Sword",
            WeaponType.one_handed_sword: "One-handed Sword",
            WeaponType.dagger: "Dagger",
            WeaponType.fishing_rod: "Fishing Rod",
            WeaponType.all: "All Weapons",
        }

    def to_dict(self) -> dict:
        return {
            "value": self.value,
            "name": self.names.get(self)
        }


class CharacterClass(enum.Enum):
    noble = "N"
    magic_knight = "K"
    court_magician = "M"

    mercenary = "W"
    gladiator = "G"
    guardian_swordsman = "D"

    saint = "S"
    priest = "P"
    shaman = "A"

    explorer = "E"
    excavator = "B"
    sniper = "H"

    @staticmethod
    def names() -> dict:
        return {
            CharacterClass.noble: "Noble",
            CharacterClass.magic_knight: "Magic Knight",
            CharacterClass.court_magician: "Court Magician",
            CharacterClass.mercenary: "Mercenary",
            CharacterClass.gladiator: "Gladiator",
            CharacterClass.guardian_swordsman: "Guardian Swordsman",
            CharacterClass.saint: "Saint",
            CharacterClass.priest: "Priest",
            CharacterClass.shaman: "Shaman",
            CharacterClass.explorer: "Explorer",
            CharacterClass.excavator: "Excavator",
            CharacterClass.sniper: "Sniper",
        }

    @classmethod
    def from_name(cls, name: str) -> "CharacterClass":
        for key, value in cls.names().items():
            if value == name:
                return key
        else:
            raise Exception(f"Name {name} was not found in enum.")

    def to_dict(self) -> dict:
        return {
            "value": self.value,
            "name": self.names().get(self)
        }


class SealOptionType(enum.Enum):
    coat = "so001"
    pants = "so002"
    gauntlet = "so003"
    shoes = "so004"
    necklace = "so005"
    ring = "so006"
    earring = "so007"
    dagger = "so008"
    one_handed_sword = "so009"
    two_handed_sword = "so010"
    rapier = "so011"
    cariad = "so012"
    duals = "so013"
    rifle = "so014"


class ProductionType(enum.Enum):
    weapon_smith = 0
    armor_smith = 1
    alchemist = 2
    workmanship = 3
    essence = 4

    @property
    def names(self) -> dict:
        return {
            ProductionType.weapon_smith: "Weapon Smith",
            ProductionType.armor_smith: "Armor Smith",
            ProductionType.alchemist: "Alchemist",
            ProductionType.workmanship: "Workmanship",
            ProductionType.essence: "Essence",
        }

    def to_dict(self) -> dict:
        return {
            "value": self.value,
            "name": self.names.get(self)
        }


class EffectCode(enum.Enum):
    max_hp = 0
    max_mp = 1

    hp_recovery = 2
    mp_recovery = 3

    avoidance_rate = 4
    movement_speed = 5

    melee_max_attack = 6
    melee_min_attack = 7
    range_max_attack = 8
    range_min_attack = 9
    magic_max_attack = 10
    magic_min_attack = 11

    physical_defense = 12
    magic_defense = 13

    melee_hitting = 14
    range_hitting = 15
    magic_hitting = 16

    melee_attack_speed = 17
    range_attack_speed = 18
    magic_attack_speed = 19

    melee_attack_range = 20
    range_attack_range = 21
    magic_attack_range = 22

    melee_critical_rate = 23
    range_critical_rate = 24
    magic_critical_rate = 25

    view_range = 26
    physical_damage_decrease = 56

    elemental_attack = 27
    illusion_attack = 28
    holy_attack = 29
    dark_attack = 30

    elemental_regeneration = 31
    illusion_regeneration = 32
    holy_regeneration = 33
    dark_regeneration = 34

    stun_state = 35
    sleep_state = 36
    silent_state = 37
    bleed_state = 38
    ice_shield_state = 52
    cannot_control_state = 59  # Confused State
    ignore_damage_state = 60  # Probably armor effect
    cannot_attack_state = 61  # Cannot attack
    resize_state = 62  # Changes character size
    slave_state = 63  # Temptation
    reflect_damage_state = 123  # Thorn shield?
    double_damage_state = 125  # Take double damage for x amount or time

    hp_recovery_intervall_3 = 39  # Regenerates hp every 3 seconds
    damage_intervall_5 = 57  # Damage every 5 seconds
    poison_intervall_8 = 58  # Posion damage every 8 seconds
    hp_alter_intervall_3 = 127  # Changes hp every 3 seconds
    mp_alter_intervall_3 = 128  # Changes mp every 3 seconds

    # Pots?
    item_hp_recovery_intervall_3 = 150
    item_mp_recovery_intervall_3 = 151
    item_dp_recovery_intervall_3 = 152
    item_en_recovery_intervall_3 = 153

    # I don't know what those are, in QA it was once mentioned that
    # they should increase skill level of those skills that need the
    # weapons / shield.
    shield_specialization = 64
    one_handed_sword_specialization = 65
    two_handed_sword_specialization = 66
    rifle_specialization = 67
    duals_specialization = 68

    recovery_skill_up = 69  # Heal increase

    # Ignores mp? idk
    # AHA Translation -> "MP invalidation (when using a skill, MP
    # consumption is invalidated)"
    ignore_mp = 70

    half_damage = 71  # Reduces damage taken by half for x specific amount
    half_cast_time = 72  # Reduces cast time by half for x specific amount

    skill_hit_rate = 73  # Increases skill hitrate

    land_exp = 113
    sea_exp = 114

    # Ignores the specific exp bonuses? -> Unknown
    land_exp_penalty = 115
    sea_exp_penalty = 116

    # AHA Translation:
    # "Fishing bite increase:
    # Fishing success rate code. 80% basic fishing success rate
    # The code uses the + value. It is a format in which % is
    # added as much as + value."
    fishing_bait_increase = 117
    fishing_bait_effectivity = 118  # Fishing bait level
    fishing_speed_increase = 154  # e.g. 0.6 = 60% faster

    stun_resistance = 119  # Resistance to stun like Absolut Defense
    stun_probability = 121  # Balance Up?

    character_critical_damage = 120

    damage_to_mp = 122  # When attacked, it reduces MP instead of HP.

    mp_usage = 124  # MP usage (+ increase,-decrease)

    total_attack = 43  # Increases all attack
    all_attack_increase = 129  # Base, Min and Max Damage
    all_defense_increase = 130  # "Total" Defense
    all_attack_speed_increase = 131

    # Used by royal slave skill
    pet_physical_defense = 132
    pet_magic_defense = 133

    # I have no clue why does are called 'attr'
    # and what that means.. :)
    attr_physical_attack = 134
    attr_posion_attack = 135
    attr_fire_attack = 136
    attr_ice_attack = 137
    attr_lightning_attack = 138
    attr_holy_attack = 139
    attr_dark_attack = 140
    attr_absolute_attack = 141

    attr_physical_regeneration = 142
    attr_posion_regeneration = 143
    attr_fire_regeneration = 144
    attr_ice_regeneration = 145
    attr_lightning_regeneration = 146
    attr_holy_regeneration = 147
    attr_dark_regeneration = 148
    attr_absolute_regeneration = 149

    all_stat_increase = 126
    constitution = 155
    strength = 156
    intelligence = 157
    dexterity = 158
    wisdom = 159
    will = 160
    luck = 161

    # UNKNOWNS but needed for some objects
    unknown_0 = 41
    unknown_1 = 111

    unknown_2 = 40
    unknown_3 = 42
    unknown_4 = 44
    unknown_5 = 45
    unknown_6 = 46
    unknown_7 = 47
    unknown_8 = 48
    unknown_9 = 49
    unknown_10 = 50
    unknown_11 = 51
    unknown_12 = 53
    unknown_13 = 54
    unknown_14 = 55
    unknown_15 = 74
    unknown_16 = 75
    unknown_17 = 76
    unknown_18 = 77
    unknown_19 = 78
    unknown_20 = 79
    unknown_21 = 80
    unknown_22 = 81
    unknown_23 = 82
    unknown_24 = 83
    unknown_25 = 84
    unknown_26 = 85
    unknown_27 = 86
    unknown_28 = 87
    unknown_29 = 88
    unknown_30 = 89
    unknown_31 = 90
    unknown_32 = 91
    unknown_33 = 92
    unknown_34 = 93
    unknown_35 = 94
    unknown_36 = 95
    unknown_37 = 96
    unknown_38 = 97
    unknown_39 = 98
    unknown_40 = 99
    unknown_41 = 100
    unknown_42 = 101
    unknown_43 = 102
    unknown_44 = 103
    unknown_45 = 104
    unknown_46 = 105
    unknown_47 = 106
    unknown_48 = 107
    unknown_49 = 108
    unknown_50 = 109
    unknown_51 = 110
    unknown_52 = 112

    # Sea stuff probably
    unknown_53 = 162
    unknown_54 = 163
    unknown_55 = 164
    unknown_56 = 165
    unknown_57 = 166
    unknown_58 = 167
    unknown_59 = 168
    unknown_60 = 169
    unknown_61 = 170
    unknown_62 = 171
    unknown_63 = 172
    unknown_64 = 173
    unknown_65 = 174

    @property
    def names(self) -> dict:
        return {
            EffectCode.max_hp: "Max. HP",
            EffectCode.max_mp: "Max. MP",
            EffectCode.hp_recovery: "HP. Recovery",
            EffectCode.mp_recovery: "MP. Recovery",
            EffectCode.avoidance_rate: "Avoidance",
            EffectCode.movement_speed: "Movement Speed",
            EffectCode.melee_max_attack: "Melee Max. Attack",
            EffectCode.melee_min_attack: "Melee Min. Attack",
            EffectCode.range_max_attack: "Range Max. Attack",
            EffectCode.range_min_attack: "Range Min. Attack",
            EffectCode.magic_max_attack: "Magic Max. Attack",
            EffectCode.magic_min_attack: "Magic Min. Attack",
            EffectCode.physical_defense: "Physical Defense",
            EffectCode.magic_defense: "Magic Defense",
            EffectCode.melee_hitting: "Melee Hitting",
            EffectCode.magic_hitting: "Magic Hitting",
            EffectCode.range_hitting: "Range Hitting",
            EffectCode.melee_attack_speed: "Melee Atk. Speed",
            EffectCode.range_attack_speed: "Range Akt. Speed",
            EffectCode.magic_attack_speed: "Magic Akt. Speed",
            EffectCode.magic_attack_range: "Magic Akt. Range",
            EffectCode.melee_attack_range: "Melee Akt. Range",
            EffectCode.range_attack_range: "Range Akt. Range",
            EffectCode.melee_critical_rate: "Melee Critical Rate",
            EffectCode.range_critical_rate: "Range Critical Rate",
            EffectCode.magic_critical_rate: "Magic Critical Rate",
            EffectCode.recovery_skill_up: "Recovery Skill Up",
            EffectCode.land_exp: "Land EXP",
            EffectCode.sea_exp: "Sea EXP",
            EffectCode.fishing_bait_effectivity: "Fishing Bait Effectivity",
            EffectCode.fishing_bait_increase: "Fishing Rate",
            EffectCode.fishing_speed_increase: "Fishing Time Decrease",
            EffectCode.total_attack: "Total Attack",
            EffectCode.all_attack_increase: "All Attack",
            EffectCode.all_defense_increase: "All Defense",
            EffectCode.all_attack_speed_increase: "Atk. Speed",
            EffectCode.all_stat_increase: "All Stat",
            EffectCode.constitution: "Constitution",
            EffectCode.strength: "Strength",
            EffectCode.intelligence: "Intelligence",
            EffectCode.dexterity: "Dexterity",
            EffectCode.wisdom: "Wisdom",
            EffectCode.will: "Will",
            EffectCode.luck: "Luck",
        }

    def to_dict(self) -> dict:
        return {
            "value": self.value,
            "name": self.names.get(self, f"?? ({self.value})")
        }
