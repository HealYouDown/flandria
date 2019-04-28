BASE_SORT_OPTIONS = {
    "Added": "added",
    "Name": "name",
}

WEAPON_OPTIONS = {
    "sort_options": {
        **BASE_SORT_OPTIONS,
        "Land Level": "level_land",
        "Sea Level": "level_sea",
    },
    "filter_options": {
        "All": "all",
        "Noble": "class_land:noble",
        "Magic Knight": "class_land:magic knight",
        "Court Magican": "class_land:court magican",
        "Mercenary": "class_land:mercenary",
        "Gladiator": "class_land:gladiator",
        "Guardian Swordman": "class_land:guardian swordman",
        "Saint": "class_land:saint",
        "Priest": "class_land:priest",
        "Shaman": "class_land:shaman",
        "Explorer": "class_land:explorer",
        "Excavator": "class_land:excavator",
        "Sniper": "class_land:sniper",
    },
}

ARMOR_OPTIONS = {
    "sort_options": {
        **BASE_SORT_OPTIONS,
        "Land Level": "level_land",
        "Sea Level": "level_sea",
    },
    "filter_options": {
        "All": "all",
        "Noble": "class_land:noble",
        "Magic Knight": "class_land:magic knight",
        "Court Magican": "class_land:court magican",
        "Mercenary": "class_land:mercenary",
        "Gladiator": "class_land:gladiator",
        "Guardian Swordman": "class_land:guardian swordman",
        "Saint": "class_land:saint",
        "Priest": "class_land:priest",
        "Shaman": "class_land:shaman",
        "Explorer": "class_land:explorer",
        "Excavator": "class_land:excavator",
        "Sniper": "class_land:sniper",
    },
}

SEA_1_OPTIONS = {
    "sort_options": {
        **BASE_SORT_OPTIONS,
        "Level": "level_sea",
    },
    "filter_options": {},
}

SEA_2_OPTIONS = {
    "sort_options": {
        **BASE_SORT_OPTIONS,
        "Level": "level_sea",
    },
    "filter_options": {
        "All": "all",
        "Armored Ship": "class_sea:armored ship",
        "Big Gun Ship": "class_sea:big gun ship",
        "Torpedo Ship": "class_sea:torpedo ship",
        "Maintenance Ship": "class_sea:maintenance ship",
        "Assault Ship": "class_sea:assault ship",
    },
}

#############

OPTIONS = {
    "monster": {
        "sort_options": {
            **BASE_SORT_OPTIONS,
            "Level": "level",
            "HP": "hp",
            "Experience": "experience",
            "Min. Dmg": "min_dmg",
            "Max. Dmg": "max_dmg",
        },
        "filter_options": {
            "All": "all",
            "Land": "location:0",
            "Sea": "location:1",
            "Island Boss": "rating_type:3",
            "Boss": "rating_type:2",
            "Elite Monster": "rating_type:1",
            "Normal Monster": "rating_type:0",
        }
    },
    # Weapons
    "cariad": WEAPON_OPTIONS,
    "rapier": WEAPON_OPTIONS,
    "dagger": WEAPON_OPTIONS,
    "one_handed_sword": WEAPON_OPTIONS,
    "two_handed_sword": WEAPON_OPTIONS,
    "shield": WEAPON_OPTIONS,
    "rifle": WEAPON_OPTIONS,
    "duals": WEAPON_OPTIONS,
    # Armor
    "coat": ARMOR_OPTIONS,
    "pants": ARMOR_OPTIONS,
    "gauntlet": ARMOR_OPTIONS,
    "shoes": ARMOR_OPTIONS,
    "quest": {
        "sort_options": {
            **BASE_SORT_OPTIONS,
            "Level": "level",
        },
        "filter_options": {
            "All": "all",
            "Land": "location:0",
            "Sea": "location:1"
        },
    },
    "quest_scroll": {
        "sort_options": {
            **BASE_SORT_OPTIONS,
        },
        "filter_options": {},
    },
    "quest_item": {
        "sort_options": {
            **BASE_SORT_OPTIONS,
        },
        "filter_options": {},
    },
    "hat": {
        "sort_options": {
            **BASE_SORT_OPTIONS,
        },
        "filter_options": {},
    },
    "dress": {
        "sort_options": {
            **BASE_SORT_OPTIONS,
        },
        "filter_options": {},
    },
    "accessory": {
        "sort_options": {
            **BASE_SORT_OPTIONS,
            "Level": "level_land",
        },
        "filter_options": {},
    },
    "recipe": {
        "sort_options": {
            **BASE_SORT_OPTIONS,
        },
        "filter_options": {},
    },
    "product_book": {
        "sort_options": {
            **BASE_SORT_OPTIONS,
        },
        "filter_options": {
            "All": "all",
            "Weapon Smith": "sec_job:0",
            "Armor Smith": "sec_job:1",
            "Alchemist": "sec_job:2",
            "Workmanship": "sec_job:3",
        },
    },
    "material": {
        "sort_options": {
            **BASE_SORT_OPTIONS,
        },
        "filter_options": {},
    },
    "shell": SEA_1_OPTIONS,
    "ship_anchor": SEA_1_OPTIONS,
    "ship_body": SEA_2_OPTIONS,
    "ship_figure": SEA_1_OPTIONS,
    "ship_head_mast": SEA_2_OPTIONS,
    "ship_main_mast": SEA_2_OPTIONS,
    "ship_magic_stone": SEA_1_OPTIONS,
    "ship_front": SEA_2_OPTIONS,
    "ship_normal_weapon": SEA_2_OPTIONS,
    "ship_special_weapon": SEA_2_OPTIONS,
    "pet_combine_help": {
        "sort_options": {
            **BASE_SORT_OPTIONS,
        },
        "filter_options": {},
    },
    "pet_combine_stone": {
        "sort_options": {
            **BASE_SORT_OPTIONS
        },
        "filter_options": {},
    },
    "pet_skill_stone": {
        "sort_options": {
            **BASE_SORT_OPTIONS,
            "Level": "level"
        },
        "filter_options": {},
    },
    "pet": {
        "sort_options": {
            **BASE_SORT_OPTIONS,
        },
        "filter_options": {},
    },
    "riding_pet": {
        "sort_options": {
            **BASE_SORT_OPTIONS,
        },
        "filter_options": {},
    },
    "seal_break_help": {
        "sort_options": {
            **BASE_SORT_OPTIONS,
        },
        "filter_options": {},
    },
    "upgrade_help": {
        "sort_options": {
            **BASE_SORT_OPTIONS,
        },
        "filter_options": {},
    },
    "upgrade_crystal": {
        "sort_options": {
            **BASE_SORT_OPTIONS,
        },
        "filter_options": {},
    },
    "upgrade_stone": {
        "sort_options": {
            **BASE_SORT_OPTIONS,
        },
        "filter_options": {},
    },
    "fishing_rod": {
        "sort_options": {
            **BASE_SORT_OPTIONS,
        },
        "filter_options": {},
    },
    "fishing_material": {
        "sort_options": {
            **BASE_SORT_OPTIONS,
        },
        "filter_options": {},
    },
    "fishing_bait": {
        "sort_options": {
            **BASE_SORT_OPTIONS,
        },
        "filter_options": {},
    },
    "random_box": {
        "sort_options": {
            **BASE_SORT_OPTIONS,
        },
        "filter_options": {},
    },
    "consumable": {
        "sort_options": {
            **BASE_SORT_OPTIONS,
        },
        "filter_options": {},
    },
    "bullet": {
        "sort_options": {
            **BASE_SORT_OPTIONS,
        },
        "filter_options": {},
    },
}