import webapp.models as models

# This list includes the models that have to be populated by the
# database_updater. So models like Drop, MapPoint, .. are not
# included here.
MODELS = [
    # Monster
    models.Monster, models.MonsterSkill, models.MonsterMessage,
    # Extra Equipment
    models.Dress, models.Hat, models.Accessory,
    # Weapons
    models.Cariad, models.Rifle, models.Duals, models.Dagger,
    models.Rapier, models.TwoHandedSword, models.OneHandedSword,
    models.Shield,
    # Armor
    models.Coat, models.Pants, models.Shoes, models.Gauntlet,
    # Crafting
    models.Recipe, models.Production, models.Material, models.ProductBook,
    # Essences
    models.Essence, models.EssenceHelp,
    # Pets
    models.PetCombineHelp, models.PetCombineStone, models.PetSkillStone,
    models.PetSkill, models.Pet, models.RidingPet,
    # Enhancing
    models.SealBreakHelp, models.UpgradeHelp, models.UpgradeStone,
    models.UpgradeCrystal,
    # Fishing
    models.FishingRod, models.FishingMaterial, models.FishingBait,
    # Ship
    models.ShipAnchor, models.ShipBody, models.ShipFigure, models.ShipFlag,
    models.ShipFront, models.ShipHeadMast, models.ShipMainMast,
    models.ShipNormalWeapon, models.ShipSpecialWeapon, models.ShipShell,
    models.ShipMagicStone,
    # Sealing
    models.SealOption, models.SealOptionData,
    # Others
    models.ItemSet, models.UpgradeRule, models.RandomBox, models.NpcShopItem,
    models.Npc, models.Consumable, models.Bullet, models.Map,
    # Skills
    models.PlayerSkill, models.SkillBook,
    # Quests
    models.QuestItem, models.QuestScroll,
]

# Models that are also added to the item_list table in a shortened form.
ITEMLIST_MODELS = [
    # Extra Equipment
    models.Dress, models.Hat, models.Accessory,
    # Weapons
    models.Cariad, models.Rifle, models.Duals, models.Dagger,
    models.Rapier, models.TwoHandedSword, models.OneHandedSword,
    models.Shield,
    # Armor
    models.Coat, models.Pants, models.Shoes, models.Gauntlet,
    # Crafting
    models.Recipe, models.Material, models.ProductBook,
    # Essences
    models.Essence, models.EssenceHelp,
    # Pets
    models.PetCombineHelp, models.PetCombineStone, models.PetSkillStone,
    models.Pet,
    # Enhancing
    models.SealBreakHelp, models.UpgradeHelp, models.UpgradeStone,
    models.UpgradeCrystal,
    # Ship
    models.ShipAnchor, models.ShipBody, models.ShipFigure, models.ShipFlag,
    models.ShipFront, models.ShipHeadMast, models.ShipMainMast,
    models.ShipNormalWeapon, models.ShipSpecialWeapon, models.ShipShell,
    models.ShipMagicStone,
    # Fishing
    models.FishingRod, models.FishingMaterial, models.FishingBait,
    # Others
    models.RandomBox, models.Consumable, models.Bullet, models.SkillBook,
    # Quests
    models.QuestItem, models.QuestScroll,
]
