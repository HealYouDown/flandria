import {Fragment} from "react"

type ItemSubsProps = {
  subs: (string | null)[]
}

export function ItemSubs({subs}: ItemSubsProps) {
  return (
    <div className="mt-[3px] flex flex-wrap gap-x-1 text-sm leading-none text-foreground/70">
      {subs.map((sub, i) => {
        if (!sub) return null

        return (
          <Fragment key={sub}>
            {i >= 1 && <span>•</span>}
            <span>{sub}</span>
          </Fragment>
        )
      })}
    </div>
  )
}
