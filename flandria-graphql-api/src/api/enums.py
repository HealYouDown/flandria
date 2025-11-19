from typing import TYPE_CHECKING

import strawberry

from src.core import enums

# TODO: waiting for https://github.com/strawberry-graphql/strawberry/issues/3543 to be merged/closed
if TYPE_CHECKING:
    AccessoryType = enums.AccessoryType
    EffectCode = enums.EffectCode
    EssenceEquipType = enums.EssenceEquipType
    Gender = enums.Gender
    ItemGrade = enums.ItemGrade
    ActorGrade = enums.ActorGrade
    MonsterMessageTrigger = enums.MonsterMessageTrigger
    SecondJobType = enums.SecondJobType
    QuestMissionType = enums.QuestMissionType
    ItemFlag = enums.ItemFlag
    ItemSetSlot = enums.ItemSetSlot
    BaseClassType = enums.BaseClassType
    Model3DClass = enums.Model3DClass
    Model3DGender = enums.Model3DGender
else:
    AccessoryType = strawberry.enum(enums.AccessoryType)
    EffectCode = strawberry.enum(enums.EffectCode)
    EssenceEquipType = strawberry.enum(enums.EssenceEquipType)
    Gender = strawberry.enum(enums.Gender)
    ItemGrade = strawberry.enum(enums.ItemGrade)
    ActorGrade = strawberry.enum(enums.ActorGrade)
    MonsterMessageTrigger = strawberry.enum(enums.MonsterMessageTrigger)
    SecondJobType = strawberry.enum(enums.SecondJobType)
    QuestMissionType = strawberry.enum(enums.QuestMissionType)
    ItemFlag = strawberry.enum(enums.ItemFlag)
    ItemSetSlot = strawberry.enum(enums.ItemSetSlot)
    BaseClassType = strawberry.enum(enums.BaseClassType)
    Model3DClass = strawberry.enum(enums.Model3DClass)
    Model3DGender = strawberry.enum(enums.Model3DGender)
