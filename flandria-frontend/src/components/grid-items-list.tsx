import {cn} from "@/lib/utils"

import * as React from "react"

interface GridItemsListProps<T> {
  items: T[]
  children: (items: T[]) => React.ReactNode
  className?: string
}

export function GridItemsList<T>({
  items,
  children,
  className,
  ...props
}: GridItemsListProps<T>) {
  if (items.length === 0) {
    // TODO: make beautiful™️
    return <div>No items found.</div>
  }

  return (
    <div
      {...props}
      className={cn(
        className,
        "grid grid-cols-1 gap-x-6 gap-y-4 py-3 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4",
      )}
    >
      {children(items)}
    </div>
  )
}
