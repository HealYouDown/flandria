import {cn} from "@/lib/utils"

import * as React from "react"

interface ColsWrapperType extends React.HTMLAttributes<HTMLDivElement> {}

export function ColsWrapper({children, className, ...props}: ColsWrapperType) {
  return (
    <div
      {...props}
      className={cn(
        "grid grid-cols-1 gap-x-8 md:grid-cols-2 lg:grid-cols-3 [&>div]:mb-8 [&>div]:flex [&>div]:flex-col [&>div]:gap-y-8",
        className,
      )}
    >
      {children}
    </div>
  )
}
