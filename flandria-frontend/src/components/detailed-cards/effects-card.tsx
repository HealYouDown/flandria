import {Effect} from "@/lib/fragments/effects-fragment"

import {effectToString} from "@/utils/format-helpers"

import {
  Card,
  CardContentList,
  CardContentListItem,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

interface EffectsCardProps {
  effects: Effect[]
}

export function EffectsCard({effects}: EffectsCardProps) {
  if (!effects || effects.length === 0) return null

  return (
    <Card>
      <CardHeader>
        <CardTitle>Mods</CardTitle>
      </CardHeader>
      <CardContentList>
        {effects.map((effect) => (
          <CardContentListItem key={effect.effect_code}>
            <p>{effectToString(effect)}</p>
          </CardContentListItem>
        ))}
      </CardContentList>
    </Card>
  )
}
