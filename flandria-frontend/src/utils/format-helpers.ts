import {Effect} from "@/lib/fragments/effects-fragment"

import {formatMinutes} from "@/utils/date-helpers"

import {
  ActorGrade,
  EffectCode,
  EssenceEquipType,
  Gender,
  SecondJobType,
} from "@/gql/graphql"

import {LinkProps} from "@tanstack/react-router"

export function monsterGradeToString(grade: ActorGrade) {
  return {
    [ActorGrade.Normal]: "Normal",
    [ActorGrade.Elite]: "Elite",
    [ActorGrade.Boss]: "Boss",
    [ActorGrade.MiniBoss]: "Mini-Boss",
  }[grade]
}

export type ObjThatSupportsCharacterClass = {
  is_noble: boolean
  is_magic_knight?: boolean
  is_court_magician?: boolean
  is_mercenary: boolean
  is_gladiator?: boolean
  is_guardian_swordsman?: boolean
  is_explorer: boolean
  is_excavator?: boolean
  is_sniper?: boolean
  is_saint: boolean
  is_priest?: boolean
  is_shaman?: boolean
}
export function characterClassStringFromObject(
  obj: ObjThatSupportsCharacterClass,
): string | null {
  if (obj.is_noble && obj.is_explorer && obj.is_mercenary && obj.is_saint) {
    return "All class"
  }

  const classes = []
  if (obj.is_noble) classes.push("Noble")
  if (obj.is_magic_knight) classes.push("Magic Knight")
  if (obj.is_court_magician) classes.push("Court Magician")

  if (obj.is_mercenary) classes.push("Mercenary")
  if (obj.is_gladiator) classes.push("Gladiator")
  if (obj.is_guardian_swordsman) classes.push("Guardian Swordsman")

  if (obj.is_explorer) classes.push("Explorer")
  if (obj.is_excavator) classes.push("Excavator")
  if (obj.is_sniper) classes.push("Sniper")

  if (obj.is_saint) classes.push("Saint")
  if (obj.is_priest) classes.push("Priest")
  if (obj.is_shaman) classes.push("Shaman")

  if (classes.length === 0) return null

  return classes.join(", ")
}

export type ObjThatSupportsShipClass = {
  is_armored: boolean
  is_big_gun: boolean
  is_torpedo: boolean
  is_maintenance: boolean
  is_assault: boolean
}

export function shipClassFromObject(
  obj: ObjThatSupportsShipClass,
): string | null {
  if (
    obj.is_armored &&
    obj.is_big_gun &&
    obj.is_torpedo &&
    obj.is_maintenance &&
    obj.is_assault
  ) {
    return "All ship"
  }

  const classes = []
  if (obj.is_armored) classes.push("Armored Ship")
  if (obj.is_big_gun) classes.push("Big Gun Ship")
  if (obj.is_torpedo) classes.push("Torpedo Ship")
  if (obj.is_maintenance) classes.push("Maintenance Ship")
  if (obj.is_assault) classes.push("Assault Ship")

  if (classes.length === 0) return null

  return classes.join(", ")
}

export const effectCodeMapping: {[key in EffectCode]: string} = {
  [EffectCode.CharAddStunProb]: "스턴확률효과",
  [EffectCode.CharAllstatepoint]: "All state",
  [EffectCode.CharAllAttackForce]: "All Attack",
  [EffectCode.CharAllAttackSpeed]: "Attack Speed",
  [EffectCode.CharAllDefenceForce]: "All Defence",
  [EffectCode.CharAlterHp_3]: "지속효과(3초마다 hp 변화)",
  [EffectCode.CharAlterMp_3]: "지속효과(3초마다 mp 변화)",
  [EffectCode.CharAtkDark]: "Dark attack",
  [EffectCode.CharAtkElemental]: "Elemental attack",
  [EffectCode.CharAtkHoly]: "Holy attack",
  [EffectCode.CharAtkIllusion]: "Illusion attack",
  [EffectCode.CharAttributeAtkAbsolute]: "절대 속성 공격력",
  [EffectCode.CharAttributeAtkDark]: "암흑 속성 공격력",
  [EffectCode.CharAttributeAtkFire]: "화염 속성 공격력",
  [EffectCode.CharAttributeAtkHoly]: "신성 속성 공격력",
  [EffectCode.CharAttributeAtkIce]: "얼음 속성 공격력",
  [EffectCode.CharAttributeAtkLightning]: "전격 속성 공격력",
  [EffectCode.CharAttributeAtkPhysical]: "물리 속성 공격력",
  [EffectCode.CharAttributeAtkPoison]: "독 속성 공격력",
  [EffectCode.CharAttributeRegAbsolute]: "절대 속성 저항력",
  [EffectCode.CharAttributeRegDark]: "암흑 속성 저항력",
  [EffectCode.CharAttributeRegFire]: "화염 속성 저항력",
  [EffectCode.CharAttributeRegHoly]: "신성 속성 저항력",
  [EffectCode.CharAttributeRegIce]: "얼음 속성 저항력",
  [EffectCode.CharAttributeRegLightning]: "전격 속성 저항력",
  [EffectCode.CharAttributeRegPhysical]: "물리 속성 저항력",
  [EffectCode.CharAttributeRegPoison]: "독 속성 저항력",
  [EffectCode.CharCannotAttak]: "Unable to attack",
  [EffectCode.CharCannotControl]: "Confusion (can't control the own will)",
  [EffectCode.CharContinueSlave]:
    "Maintains the slave state for a certain time.",
  [EffectCode.CharCridmg]: "크리티컬데미지 상승",
  [EffectCode.CharDamagex2]: "공격받으면 2배의 데미지를 받음",
  [EffectCode.CharDamage_5]: "Character's HP decrease every 5 seconds",
  [EffectCode.CharDamageAlterMp]: "HP대신 MP 감소",
  [EffectCode.CharDamageToMp]: "It absorbs n% of damage to MP.",
  [EffectCode.CharFishingBaitPerformance]: "낚시 미끼성능(미끼레벨)",
  [EffectCode.CharFishingSpeedup]: "Fishing Time Decrease",
  [EffectCode.CharHalfCastingtime]:
    "Casting time is decreased by 50% (managing the number of using)",
  [EffectCode.CharHalfDamge]:
    "All damage is decreased by 50% (managing the number of decreased damage)",
  [EffectCode.CharIceShield]:
    "Ice shield effect (Until the ice is broken, HP do not decrease.)",
  [EffectCode.CharIgnoreDamage]: "Ignore damage (HP are not decreased)",
  [EffectCode.CharIgnoreUsemp]: "Ignore used MP",
  [EffectCode.CharMagicCriRate]: "Magic critical rate",
  [EffectCode.CharMagicDefc]: "Magic resistance",
  [EffectCode.CharMagicDst]: "Magic distance",
  [EffectCode.CharMagicHit]: "Magic hitting",
  [EffectCode.CharMagicMaxAttk]: "Magic max attack",
  [EffectCode.CharMagicMinAttk]: "Magic min attack",
  [EffectCode.CharMagicSpd]: "Magic attack speed",
  [EffectCode.CharMaxHp]: "Max HP",
  [EffectCode.CharMaxMp]: "Max MP",
  [EffectCode.CharMeleeCriRate]: "Melee critical rate",
  [EffectCode.CharMeleeDst]: "Melee distance",
  [EffectCode.CharMeleeHit]: "Melee hitting",
  [EffectCode.CharMeleeMaxAttk]: "Melee max attack",
  [EffectCode.CharMeleeMinAttk]: "Melee min attack",
  [EffectCode.CharMeleeSpd]: "Melee speed",
  [EffectCode.CharMoveSpd]: "Moving speed",
  [EffectCode.CharMpcost]: "MP Cost",
  [EffectCode.CharOnehandSpecialize]: "One-hand specialization",
  [EffectCode.CharPassExppenalty]: "육상 경험치 패널티 적용되지 않는 효과",
  [EffectCode.CharPhdamageDecrease]: "Physical damage",
  [EffectCode.CharPhAvd]: "Physical avoidance rate",
  [EffectCode.CharPhDefc]: "Physical defence",
  [EffectCode.CharPistolSpecialize]: "Gun specialization",
  [EffectCode.CharPoisonDamage_8]: "Decrease HP by poison every 5 seconds",
  [EffectCode.CharRangeCriRate]: "Range critical rate",
  [EffectCode.CharRangeDst]: "Range distance",
  [EffectCode.CharRangeHit]: "Long range hitting",
  [EffectCode.CharRangeMaxAttk]: "Range max attack",
  [EffectCode.CharRangeMinAttk]: "Range min attack",
  [EffectCode.CharRangeSpd]: "Range attack speed",
  [EffectCode.CharRecoveryHp_3]: "HP recovery per 3 seconds",
  [EffectCode.CharRecoverySkillUp]: "Recovery skill up",
  [EffectCode.CharRegistStun]: "스턴저항",
  [EffectCode.CharRegDark]: "Dark resistance",
  [EffectCode.CharRegElemental]: "Elemental resistance",
  [EffectCode.CharRegHoly]: "Holy resistance",
  [EffectCode.CharRegIllusion]: "Illusion  resistance",
  [EffectCode.CharResize]: "Change of character size",
  [EffectCode.CharRevHp]: "HP recovery",
  [EffectCode.CharRevMp]: "MP recovery",
  [EffectCode.CharRifleSpecialize]: "Rifle specialization",
  [EffectCode.CharShieldSpecialize]: "Shield specialization",
  [EffectCode.CharSkillHitrateUp]: "increases the success rate of skills",
  [EffectCode.CharStateBleed]: "Bleed",
  [EffectCode.CharStateSilent]: "Silent",
  [EffectCode.CharStateStun]: "Stun",
  [EffectCode.CharStateSwoon]: "Swoon",
  [EffectCode.CharTaunt]: "Taunt add (8/15)",
  [EffectCode.CharTwohandSpecialize]: "Two-hand specialization",
  [EffectCode.CharUpFishingBait]: "Fishing Rate",
  [EffectCode.CharViewRange]: "View range",
  [EffectCode.CharWhenAttackingDamage]: "공격할때 피해(데미지)를 당한다.",
  [EffectCode.Con]: "Constitution",
  [EffectCode.Dex]: "Dexterity",
  [EffectCode.IncreateRewardexpLand]: "Land EXP",
  [EffectCode.IncreateRewardexpSea]: "Sea EXP",
  [EffectCode.Int]: "Intelligence",
  [EffectCode.Luc]: "Luck",
  [EffectCode.PetMagicDefc]: "팻 마법 저항력",
  [EffectCode.PetPhDefc]: "팻 물리 방어력",
  [EffectCode.ShipDamage_3]: "Damage per 3 seconds",
  [EffectCode.ShipDownMaxMovespeed]: "Ship moving speed",
  [EffectCode.ShipDownTurnSpeed]: "Ship turning speed",
  [EffectCode.ShipImpossibleTurn]: "Turning is impossible",
  [EffectCode.ShipNeedenergySpecialweapon]: "special consumption of EN",
  [EffectCode.ShipPassExppenalty]: "해상 경험치 패널티 적용되지 않는 효과",
  [EffectCode.ShipStun]: "Ship stun effect",
  [EffectCode.ShipUpdownAllAttack]: "Total attack",
  [EffectCode.ShipUpdownAttributeAttack]: "Attribute attack",
  [EffectCode.ShipUpdownCannonAttackDist]: "Ship cannon attack distance",
  [EffectCode.ShipUpdownCollusionDamage]: "Damage of ship collusion",
  [EffectCode.ShipUpdownDefence]: "Defence",
  [EffectCode.ShipUpdownMeleeAttack]: "Melee attack",
  [EffectCode.ShipUpdownRangeAttack]: "Range attack",
  [EffectCode.ShipUpdownShellThrongRange]: "Shell throng range",
  [EffectCode.ShipUpAcceleration]: "Acceleration power",
  [EffectCode.ShipUpBalance]: "Balance effect",
  [EffectCode.ShipUpBombatk]: "Explosive power",
  [EffectCode.ShipUpCannonatk]: "Cannon attack power",
  [EffectCode.ShipUpCannoncritical]: "Cannon critical",
  [EffectCode.ShipUpCannoneffectivedist]: "Cannon effective dist",
  [EffectCode.ShipUpCannonmaxdist]: "Cannon max dist",
  [EffectCode.ShipUpCannonproof]: "Cannon proof power",
  [EffectCode.ShipUpCannonreload]: "Cannon reload time",
  [EffectCode.ShipUpCannonshellrange]: "Cannon shell range",
  [EffectCode.ShipUpCannonshellspeed]: "Cannon shell speed",
  [EffectCode.ShipUpCrashatk]: "Crash power",
  [EffectCode.ShipUpDefence]: "Defence power",
  [EffectCode.ShipUpDestroyatk]: "Destroy power",
  [EffectCode.ShipUpDoubledamage]: "Double striking power",
  [EffectCode.ShipUpDurabilityblind]: "Continuously blind",
  [EffectCode.ShipUpDurabilityflash]: "Continuous Flash",
  [EffectCode.ShipUpEffectdefence]: "No status change",
  [EffectCode.ShipUpGunatk]: "Gun attack power",
  [EffectCode.ShipUpGuncritial]: "Gun critial",
  [EffectCode.ShipUpGunmaxdist]: "Gun max distance",
  [EffectCode.ShipUpGunreload]: "Gun reload time",
  [EffectCode.ShipUpHeadwindresist]: "Headwind resistance",
  [EffectCode.ShipUpHidenotarget]: "Hide",
  [EffectCode.ShipUpHprecovery]: "DP recovery",
  [EffectCode.ShipUpMaxhp]: "Max DP",
  [EffectCode.ShipUpMaxmp]: "Max EN",
  [EffectCode.ShipUpMaxDura]: "Max dura is increased",
  [EffectCode.ShipUpMaxMovespeed]: "Ship moving speed",
  [EffectCode.ShipUpMprecovery]: "EN recovery",
  [EffectCode.ShipUpNoskill]: "Skill is not used",
  [EffectCode.ShipUpPiercingatk]: "Piercing power",
  [EffectCode.ShipUpRegbomb]: "Explosive resistance",
  [EffectCode.ShipUpRegcrash]: "Crash resistance",
  [EffectCode.ShipUpRegdestroy]: "Destroy resistance",
  [EffectCode.ShipUpRegpiercing]: "Through resistance",
  [EffectCode.ShipUpRetardation]: "Retardation power",
  [EffectCode.ShipUpShipavoid]: "Auto avoidance",
  [EffectCode.ShipUpSpecialcritical]: "Special critical",
  [EffectCode.ShipUpSpecialforceatk]: "Special force attack",
  [EffectCode.ShipUpSpecialmaxdist]: "Special max distance",
  [EffectCode.ShipUpSpecialshellspeed]: "Special shell speed",
  [EffectCode.ShipUpSpeedForeaftsail]: "Foreafter sail",
  [EffectCode.ShipUpSpeedSquaresail]: "Square sail",
  [EffectCode.ShipUpTurnspeed]: "Turning power",
  [EffectCode.ShipUpTurnSpeed]: "Increase turning speed",
  [EffectCode.Str]: "Strength",
  [EffectCode.Unknown_1]: "UNKNOWN_1",
  [EffectCode.Unknown_2]: "UNKNOWN_2",
  [EffectCode.Unknown_3]: "UNKNOWN_3",
  [EffectCode.Unknown_4]: "UNKNOWN_4",
  [EffectCode.Unknown_5]: "UNKNOWN_5",
  [EffectCode.Unknown_6]: "UNKNOWN_6",
  [EffectCode.Unknown_7]: "UNKNOWN_7",
  [EffectCode.Unknown_8]: "UNKNOWN_8",
  [EffectCode.Unknown_9]: "UNKNOWN_9",
  [EffectCode.Vol]: "Will",
  [EffectCode.Wis]: "Wisdom",
}

export function effectCodeToString(effectCode: EffectCode): string {
  return effectCodeMapping[effectCode]
}

export function effectToString(effect: Effect) {
  const effectName = effectCodeToString(effect.effect_code)
  let valueString
  if (effect.operator === "+" || effect.operator === "-") {
    valueString = `${effect.operator}${effect.value}`
  } else if (effect.operator === "*") {
    valueString = `${(effect.value * 100).toFixed(0)}%`
  }

  return `${effectName} ${valueString}`
}

export function genderToString(gender: Gender) {
  return {
    [Gender.Genderless]: "Male, Female",
    [Gender.Male]: "Male",
    [Gender.Female]: "Female",
  }[gender]
}

export function essenceEquipTypeToString(et: EssenceEquipType) {
  return {
    [EssenceEquipType.All]: "Equip: All",
    [EssenceEquipType.Armor]: "Equip: Armor",
    [EssenceEquipType.Dress]: "Equip: Dress",
    [EssenceEquipType.DressArmor]: "Equip: Dress, Armor",
    [EssenceEquipType.DressArmorShield]: "Equip: Dress, Armor, Shield",
    [EssenceEquipType.DressWeaponsArmor]: "Equip: Dress, Weapon, Armor",
    [EssenceEquipType.Shield]: "Equip: Shield",
    [EssenceEquipType.Weapons]: "Equip: Weapons",
    [EssenceEquipType.WeaponsArmor]: "Equip: Weapons, Armor",
    [EssenceEquipType.WeaponsShield]: "Equip: Weapons, Shield",
  }[et]
}

export type TablenameLinkMapping = {
  [key: string]: LinkProps["to"]
}
export function rangeToMeters(range: number, factor: number = 100) {
  // for monsters and skills, its /100
  // for ship items, it's /10
  const r = (range / factor).toFixed(1)
  return r.toLocaleString()
}

export function booleanToDisplayString(bool: boolean) {
  return bool ? "Yes" : "No"
}

export function nameWithDuration(
  name: string,
  durationMinutes?: number | null,
) {
  if (durationMinutes) {
    return name + ` (${formatMinutes(durationMinutes)})`
  }
  return name
}

export function productionTypeToString(type: SecondJobType): string {
  return {
    [SecondJobType.Alchemist]: "Alchemist",
    [SecondJobType.ArmorSmith]: "Armor Smith",
    [SecondJobType.WeaponSmith]: "Weapon Smith",
    [SecondJobType.Workmanship]: "Workmanship",
    [SecondJobType.Essence]: "Essence",
  }[type]
}

export function formatSkillRequiredWeapons(s: string): string {
  const weaponNames: string[] = []

  s.split("").forEach((j) => {
    if (j === "P") weaponNames.push("Duals")
    else if (j === "R") weaponNames.push("Rifle")
    else if (j === "C") weaponNames.push("Cariad")
    else if (j === "B") weaponNames.push("Shield")
    else if (j === "A") weaponNames.push("Rapier")
    else if (j === "T") weaponNames.push("Two-handed Sword")
    else if (j === "S") weaponNames.push("One-handed Sword")
    else if (j === "D") weaponNames.push("Dagger")
    else if (j === "F") weaponNames.push("Fishing Rod")
    else if (j === "X") weaponNames.push("All Weapons")
  })

  if (weaponNames.length === 0) return "All Weapons"

  return weaponNames.join(", ")
}
