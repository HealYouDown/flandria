import {Effect} from "@/lib/fragments/effects-fragment"

import {effectToString} from "@/utils/format-helpers"

import {Fragment} from "react"

type ItemSubsProps = {
  effects: Effect[]
}

export function ItemEffects({effects}: ItemSubsProps) {
  if (effects.length === 0) return null

  return (
    <div className="flex flex-wrap gap-x-1 text-xs text-[#267e81] dark:text-[#00f7ff]/80">
      {effects.map((effect, i) => (
        <Fragment key={effect.effect_code}>
          {i >= 1 && <span>•</span>}
          <span className="whitespace-nowrap">{effectToString(effect)}</span>
        </Fragment>
      ))}
    </div>
  )
}
