import {cn} from "@/lib/utils"

import {isAprilFools} from "@/utils/date-helpers"

import {ActorGrade, ItemGrade} from "@/gql/graphql"

import {type VariantProps, cva} from "class-variance-authority"
import * as React from "react"

const actorGradeBorderClassLookup = {
  [ActorGrade.Normal]: "border-border",
  [ActorGrade.Elite]: "border-[#7fce2e]",
  [ActorGrade.MiniBoss]: "border-[#cf304e]",
  [ActorGrade.Boss]: "border-[#e7b23f]",
}

const itemGradeBorderClassLookup = {
  [ItemGrade.Blue]: "border-[#99ccff]",
  [ItemGrade.Green]: "border-[#99e680]",
  [ItemGrade.Yellow]: "border-[#e6cc99]",
  [ItemGrade.Orange]: "border-[#ffbd8f]",
}

const iconVariants = cva("w-10 h-10 border-2 rounded-xl", {
  variants: {
    variant: {
      "default":
        "transition-all border-opacity-50 group-hover:border-opacity-100",
      "no-hover": "",
    },
    size: {
      default: "w-10 h-10",
      medium: "w-8 h-8",
      small: "w-6 h-6",
    },
  },
  defaultVariants: {
    size: "default",
    variant: "default",
  },
})

interface ItemIconProps extends VariantProps<typeof iconVariants> {
  iconName: string
  actorGrade?: ActorGrade
  itemGrade?: ItemGrade
  className?: string
}

export function ItemIcon({
  iconName,
  actorGrade,
  itemGrade,
  size,
  variant,
  className,
}: ItemIconProps) {
  const [hasError, setHasError] = React.useState(false)

  let borderColorClass = "border-border"
  if (actorGrade) {
    borderColorClass = actorGradeBorderClassLookup[actorGrade]
  }
  if (itemGrade) {
    borderColorClass = itemGradeBorderClassLookup[itemGrade]
  }
  const iconClassName = cn(
    iconVariants({size, variant, className: cn(borderColorClass, className)}),
  )

  // Celty and I had a discussion about what we should do on 1st April... so here we are :)
  const finalIconName = isAprilFools() ? "ieu_137.png" : iconName

  let icon: JSX.Element | null = (
    <img
      className={iconClassName}
      src={`/assets/icons/${finalIconName}`}
      onError={() => setHasError(true)}
    />
  )

  if (hasError) {
    // For actors, we have a fallback icon. For items we don't.
    const isActorIcon = actorGrade !== undefined
    if (isActorIcon) {
      icon = <img className={iconClassName} src={`/assets/icons/npcface.png`} />
    } else {
      icon = null
    }
  }

  return icon
}
