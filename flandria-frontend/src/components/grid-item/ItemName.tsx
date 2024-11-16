import {cn} from "@/lib/utils"

import {formatMinutes} from "@/utils/date-helpers"

interface ItemNameProps extends React.ComponentProps<"span"> {
  duration?: number | null
}

export function ItemName({
  children,
  className,
  duration: durationInMinutes,
  ...props
}: ItemNameProps) {
  return (
    <div className="flex flex-wrap items-center space-x-1">
      <span {...props} className={cn("leading-none", className)}>
        {children}
      </span>
      {durationInMinutes && (
        <span className="leading-none text-foreground/70">
          ({formatMinutes(durationInMinutes)})
        </span>
      )}
    </div>
  )
}
