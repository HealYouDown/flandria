import {BaseClassType} from "@/gql/graphql"

export function calculateMaxHP(
  lv: number,
  characterClass: BaseClassType,
  con: number,
): number {
  if (characterClass === BaseClassType.Mercenary) {
    return Math.floor(
      Math.pow(lv * 13.0, 1.2) + Math.pow((con - 13) * 13.0, 1.2) - 50,
    )
  } else if (characterClass === BaseClassType.Explorer) {
    return Math.floor(
      Math.pow(lv * 12.0, 1.2) + Math.pow((con - 9) * 13.0, 1.2) + 20,
    )
  } else if (characterClass === BaseClassType.Noble) {
    return Math.floor(
      Math.pow(lv * 12.0, 1.2) + Math.pow((con - 4) * 10.0, 1.2) + 40,
    )
  } else if (characterClass === BaseClassType.Saint) {
    return Math.floor(
      Math.pow(lv * 12.0, 1.2) + Math.pow((con - 6) * 11.0, 1.2) + 20,
    )
  }

  throw new Error("Unknown base class")
}

export function calculateMaxMP(
  lv: number,
  characterClass: BaseClassType,
  wis: number,
): number {
  if (
    characterClass === BaseClassType.Mercenary ||
    characterClass === BaseClassType.Explorer
  ) {
    return Math.pow(lv * 10.0, 1.2) + Math.pow((wis - 6) * 10.0, 1.2) + 60
  } else if (
    characterClass === BaseClassType.Noble ||
    characterClass === BaseClassType.Saint
  ) {
    return Math.pow(lv * 11.0, 1.2) + Math.pow((wis - 13) * 12.0, 1.2) + 60
  }
  throw new Error("Unknown base class")
}

export function calculateMeleeMinAttack(
  lv: number,
  characterClass: BaseClassType,
  str: number,
  int: number,
): number {
  if (characterClass === BaseClassType.Mercenary) {
    return Math.pow(lv, 1.1) + Math.pow((str - 10) * 1.5, 1.1) - 10
  } else if (characterClass === BaseClassType.Explorer) {
    return Math.pow(lv, 1.1) + Math.pow((str - 9) * 1.4, 1.1) - 11
  } else if (characterClass === BaseClassType.Noble) {
    return (
      Math.pow(lv, 1.1) +
      Math.pow((str - 6) * 1.4, 1.1) +
      Math.pow((int - 12) * 0.8, 1.1) -
      10
    )
  } else if (characterClass === BaseClassType.Saint) {
    return (
      Math.pow(lv, 1.1) +
      Math.pow((str - 6) * 1.4, 1.1) +
      Math.pow((int - 12) * 0.8, 1.1) -
      8
    )
  }

  throw new Error("Unknown base class")
}

export function calculateMeleeMaxAttack(
  lv: number,
  characterClass: BaseClassType,
  str: number,
  int: number,
): number {
  if (characterClass === BaseClassType.Mercenary) {
    return Math.pow(lv, 1.1) + Math.pow((str - 10) * 1.5, 1.1) - 10
  } else if (characterClass === BaseClassType.Explorer) {
    return Math.pow(lv, 1.1) + Math.pow((str - 9) * 1.4, 1.1) - 11
  } else if (characterClass === BaseClassType.Noble) {
    return (
      Math.pow(lv, 1.1) +
      Math.pow((str - 6) * 1.4, 1.1) +
      Math.pow((int - 12) * 0.8, 1.1) -
      10
    )
  } else if (characterClass === BaseClassType.Saint) {
    return (
      Math.pow(lv, 1.1) +
      Math.pow((str - 6) * 1.4, 1.1) +
      Math.pow((int - 12) * 0.8, 1.1) -
      8
    )
  }

  throw new Error("Unknown base class")
}

export function calculateMeleeHitRate(
  lv: number,
  characterClass: BaseClassType,
  dex: number,
): number {
  if (characterClass === BaseClassType.Mercenary) {
    return Math.pow(lv * 1.5, 1.1) + Math.pow((dex - 12) * 1.5, 1.1) + 40
  } else if (characterClass === BaseClassType.Explorer) {
    return Math.pow(lv * 1.6, 1.1) + Math.pow((dex - 12) * 1.5, 1.1) + 45
  } else if (characterClass === BaseClassType.Noble) {
    return Math.pow(lv * 2.0, 1.1) + Math.pow((dex - 9) * 2.2, 1.1) + 30
  } else if (characterClass === BaseClassType.Saint) {
    return Math.pow(lv * 2.0, 1.1) + Math.pow((dex - 9) * 2.2, 1.1) + 35
  }

  throw new Error("Unknown base class")
}

export function calculateMeleeCriticalRate(
  lv: number,
  characterClass: BaseClassType,
  vol: number,
): number {
  if (characterClass === BaseClassType.Mercenary) {
    return Math.pow(lv * 1.0, 1.1) + Math.pow((vol - 9) * 3.0, 1.1)
  } else if (characterClass === BaseClassType.Explorer) {
    return Math.pow(lv * 1.0, 1.1) + Math.pow((vol - 10) * 3.0, 1.1)
  } else if (characterClass === BaseClassType.Noble) {
    return Math.pow(lv * 1.0, 1.1) + Math.pow((vol - 8) * 3.0, 1.1)
  } else if (characterClass === BaseClassType.Saint) {
    return Math.pow(lv * 1.0, 1.1) + Math.pow((vol - 10) * 3.0, 1.1)
  }

  throw new Error("Unknown base class")
}

export function calculateRangedMinAttack(
  lv: number,
  characterClass: BaseClassType,
  str: number,
  int_: number,
): number {
  if (characterClass === BaseClassType.Mercenary) {
    return Math.pow(lv, 1.1) + Math.pow((str - 10) * 1.4, 1.1) - 10
  } else if (characterClass === BaseClassType.Explorer) {
    return Math.pow(lv, 1.1) + Math.pow((str - 9) * 1.5, 1.1) - 11
  } else if (characterClass === BaseClassType.Noble) {
    return (
      Math.pow(lv, 1.1) +
      Math.pow((str - 6) * 1.4, 1.1) +
      Math.pow((int_ - 12) * 0.8, 1.1) -
      10
    )
  } else if (characterClass === BaseClassType.Saint) {
    return (
      Math.pow(lv, 1.1) +
      Math.pow((str - 6) * 1.4, 1.1) +
      Math.pow((int_ - 12) * 0.8, 1.1) -
      8
    )
  }

  throw new Error("Unknown base class")
}

export function calculateRangedMaxAttack(
  lv: number,
  characterClass: BaseClassType,
  str: number,
  int_: number,
): number {
  if (characterClass === BaseClassType.Mercenary) {
    return Math.pow(lv, 1.1) + Math.pow((str - 10) * 1.4, 1.1) - 10
  } else if (characterClass === BaseClassType.Explorer) {
    return Math.pow(lv, 1.1) + Math.pow((str - 9) * 1.5, 1.1) - 11
  } else if (characterClass === BaseClassType.Noble) {
    return (
      Math.pow(lv, 1.1) +
      Math.pow((str - 6) * 1.4, 1.1) +
      Math.pow((int_ - 12) * 0.8, 1.1) -
      10
    )
  } else if (characterClass === BaseClassType.Saint) {
    return (
      Math.pow(lv, 1.1) +
      Math.pow((str - 6) * 1.4, 1.1) +
      Math.pow((int_ - 12) * 0.8, 1.1) -
      8
    )
  }

  throw new Error("Unknown base class")
}

export function calculateRangedHitRate(
  lv: number,
  characterClass: BaseClassType,
  dex: number,
): number {
  if (characterClass === BaseClassType.Mercenary) {
    return Math.pow(lv * 1.5, 1.1) + Math.pow((dex - 12) * 1.5, 1.1) + 40
  } else if (characterClass === BaseClassType.Explorer) {
    return Math.pow(lv * 1.6, 1.1) + Math.pow((dex - 12) * 1.6, 1.1) + 45
  } else if (characterClass === BaseClassType.Noble) {
    return Math.pow(lv * 2.0, 1.1) + Math.pow((dex - 9) * 2.2, 1.1) + 30
  } else if (characterClass === BaseClassType.Saint) {
    return Math.pow(lv * 2.0, 1.1) + Math.pow((dex - 9) * 2.2, 1.1) + 35
  }

  throw new Error("Unknown base class")
}

export function calculateRangedCriticalRate(
  lv: number,
  characterClass: BaseClassType,
  vol: number,
): number {
  if (characterClass === BaseClassType.Mercenary) {
    return Math.pow(lv * 1.0, 1.1) + Math.pow((vol - 9) * 3.0, 1.1)
  } else if (characterClass === BaseClassType.Explorer) {
    return Math.pow(lv * 1.0, 1.1) + Math.pow((vol - 10) * 3.0, 1.1)
  } else if (characterClass === BaseClassType.Noble) {
    return Math.pow(lv * 1.0, 1.1) + Math.pow((vol - 8) * 3.0, 1.1)
  } else if (characterClass === BaseClassType.Saint) {
    return Math.pow(lv * 1.0, 1.1) + Math.pow((vol - 10) * 3.0, 1.1)
  }

  throw new Error("Unknown base class")
}

export function calculateMagicMinAttack(
  lv: number,
  characterClass: BaseClassType,
  int_: number,
): number {
  if (characterClass === BaseClassType.Mercenary) {
    return Math.pow(lv, 1.1) + Math.pow((int_ - 5) * 1.4, 1.1)
  } else if (characterClass === BaseClassType.Explorer) {
    return Math.pow(lv, 1.1) + Math.pow((int_ - 5) * 1.4, 1.1) - 5
  } else if (characterClass === BaseClassType.Noble) {
    return Math.pow(lv, 1.1) + Math.pow((int_ - 12) * 1.6, 1.1) - 8
  } else if (characterClass === BaseClassType.Saint) {
    return Math.pow(lv, 1.1) + Math.pow((int_ - 11) * 1.6, 1.1)
  }

  throw new Error("Unknown base class")
}

export function calculateMagicMaxAttack(
  lv: number,
  characterClass: BaseClassType,
  int_: number,
): number {
  if (characterClass === BaseClassType.Mercenary) {
    return Math.pow(lv, 1.1) + Math.pow((int_ - 5) * 1.4, 1.1)
  } else if (characterClass === BaseClassType.Explorer) {
    return Math.pow(lv, 1.1) + Math.pow((int_ - 5) * 1.4, 1.1) - 5
  } else if (characterClass === BaseClassType.Noble) {
    return Math.pow(lv, 1.1) + Math.pow((int_ - 12) * 1.6, 1.1) - 8
  } else if (characterClass === BaseClassType.Saint) {
    return Math.pow(lv, 1.1) + Math.pow((int_ - 11) * 1.6, 1.1)
  }

  throw new Error("Unknown base class")
}

export function calculateMagicHitRate(
  lv: number,
  characterClass: BaseClassType,
  dex: number,
  int_: number,
): number {
  if (characterClass === BaseClassType.Mercenary) {
    return Math.pow(lv * 1.5, 1.1) + Math.pow((dex - 12) * 1.5, 1.1) + 40
  } else if (characterClass === BaseClassType.Explorer) {
    return Math.pow(lv * 1.6, 1.1) + Math.pow((dex - 13) * 1.5, 1.1) + 40
  } else if (characterClass === BaseClassType.Noble) {
    return (
      Math.pow(lv * 1.5, 1.1) +
      Math.pow((dex - 14) * 2.2, 1.1) +
      Math.pow(int_ - 14, 1.1) +
      40
    )
  } else if (characterClass === BaseClassType.Saint) {
    return (
      Math.pow(lv * 1.5, 1.1) +
      Math.pow((dex - 12) * 2.2, 1.1) +
      Math.pow(int_ - 12, 1.1) +
      45
    )
  }

  throw new Error("Unknown base class")
}

export function calculateMagicCriticalRate(
  lv: number,
  characterClass: BaseClassType,
  vol: number,
): number {
  if (characterClass === BaseClassType.Mercenary) {
    return Math.pow(lv * 1.0, 1.1) + Math.pow((vol - 9) * 3.0, 1.1)
  } else if (characterClass === BaseClassType.Explorer) {
    return Math.pow(lv * 1.0, 1.1) + Math.pow((vol - 10) * 3.0, 1.1)
  } else if (characterClass === BaseClassType.Noble) {
    return Math.pow(lv * 1.0, 1.1) + Math.pow((vol - 8) * 3.0, 1.1)
  } else if (characterClass === BaseClassType.Saint) {
    return Math.pow(lv * 1.0, 1.1) + Math.pow((vol - 10) * 3.0, 1.1)
  }

  throw new Error("Unknown base class")
}

export function calculateAvoidance(
  lv: number,
  characterClass: BaseClassType,
  dex: number,
): number {
  if (characterClass === BaseClassType.Mercenary) {
    return Math.pow(lv * 1.0, 1.1) + Math.pow((dex - 12) * 0.5, 1.1) + 6
  } else if (characterClass === BaseClassType.Explorer) {
    return Math.pow(lv * 1.2, 1.1) + Math.pow((dex - 10) * 0.6, 1.1) + 2
  } else if (characterClass === BaseClassType.Noble) {
    return Math.pow(lv * 1.2, 1.1) + Math.pow((dex - 10) * 1.0, 1.1) + 3
  } else if (characterClass === BaseClassType.Saint) {
    return Math.pow(lv * 1.2, 1.1) + Math.pow((dex - 10) * 1.0, 1.1) + 3
  }

  throw new Error("Unknown base class")
}
