import {ComboboxOption} from "@/components/combobox"
import {ClassFlagsType} from "@/components/planner/skill-helpers"

export const landLevelOptions: ComboboxOption<string>[] = [
  ...Array(105).keys(),
].map((i) => ({label: (i + 1).toString(), value: (i + 1).toString()}))

export const seaLevelOptions: ComboboxOption<string>[] = [
  ...Array(99).keys(),
].map((i) => ({label: (i + 1).toString(), value: (i + 1).toString()}))

export const explorerClassOptions: ComboboxOption<ClassFlagsType>[] = [
  {
    label: "Excavator",
    value: "is_excavator",
  },
  {
    label: "Sniper",
    value: "is_sniper",
  },
]

export const mercenaryClassOptions: ComboboxOption<ClassFlagsType>[] = [
  {
    label: "Gladiator",
    value: "is_gladiator",
  },
  {
    label: "Guardian Swordsman",
    value: "is_guardian_swordsman",
  },
]

export const nobleClassOptions: ComboboxOption<ClassFlagsType>[] = [
  {
    label: "Magic Knight",
    value: "is_magic_knight",
  },
  {
    label: "Court Magician",
    value: "is_court_magician",
  },
]

export const saintClassOptions: ComboboxOption<ClassFlagsType>[] = [
  {
    label: "Shaman",
    value: "is_shaman",
  },
  {
    label: "Priest",
    value: "is_priest",
  },
]
