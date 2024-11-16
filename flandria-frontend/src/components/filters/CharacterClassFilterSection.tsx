import {ObjThatSupportsCharacterClass} from "@/utils/format-helpers"

import {Combobox, ComboboxOption} from "@/components/combobox"
import {FilterMenuChildrenRenderProps} from "@/components/pagination-filter"

import {UseNavigateResult} from "@tanstack/react-router"
import {z} from "zod"

type CharacterClassKeys = keyof ObjThatSupportsCharacterClass
const characterClassFilterOptions: ComboboxOption<CharacterClassKeys>[] = [
  {
    label: "Noble",
    value: "is_noble",
  },
  {
    label: "Magic Knight",
    value: "is_magic_knight",
  },
  {
    label: "Court Magician",
    value: "is_court_magician",
  },
  {
    label: "Explorer",
    value: "is_explorer",
  },
  {
    label: "Excavator",
    value: "is_excavator",
  },
  {
    label: "Sniper",
    value: "is_sniper",
  },
  {
    label: "Saint",
    value: "is_saint",
  },
  {
    label: "Priest",
    value: "is_priest",
  },
  {
    label: "Shaman",
    value: "is_shaman",
  },
  {
    label: "Mercenary",
    value: "is_mercenary",
  },
  {
    label: "Gladiator",
    value: "is_gladiator",
  },
  {
    label: "Guardian Swordsman",
    value: "is_guardian_swordsman",
  },
] as const

export const characterClassValidators = z.custom<CharacterClassKeys>((val) =>
  characterClassFilterOptions.map((o) => o.value).includes(val),
)

type CharacterClassFilterSectionProps = {
  cc: CharacterClassKeys | null
  basesClassOnly?: boolean
  navigate: UseNavigateResult<"/">
} & FilterMenuChildrenRenderProps

export function CharacterClassFilterSection({
  Section,
  Label,
  cc,
  navigate,
  basesClassOnly = false,
}: CharacterClassFilterSectionProps) {
  const options = basesClassOnly
    ? characterClassFilterOptions.filter((opt) =>
        ["is_noble", "is_saint", "is_explorer", "is_mercenary"].includes(
          opt.value,
        ),
      )
    : characterClassFilterOptions

  return (
    <Section>
      <Label htmlFor="character-class">Class</Label>
      <Combobox
        nullable
        id="character-class"
        triggerClassName="col-span-2"
        value={cc}
        options={options}
        onValueChange={(value) => {
          navigate({
            search: (prev) => ({
              ...prev,
              page: 1,
              cc: value,
            }),
          })
        }}
      />
    </Section>
  )
}
