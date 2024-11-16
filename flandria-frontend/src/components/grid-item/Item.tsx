import {cn} from "@/lib/utils"

import {Slot} from "@radix-ui/react-slot"
import {createLink} from "@tanstack/react-router"
import * as React from "react"

interface ItemProps extends React.AnchorHTMLAttributes<HTMLAnchorElement> {}

const Item_ = React.forwardRef<HTMLAnchorElement, ItemProps>(
  ({className, children, ...props}, ref) => (
    <a
      ref={ref}
      {...props}
      className={cn(
        "group flex items-center gap-2 hover:animate-scale",
        className,
      )}
    >
      {children}
    </a>
  ),
)

export const Item = createLink(Item_)

export const NonLinkItem = ({
  children,
  className,
  asChild = false,
}: React.PropsWithChildren & {className?: string; asChild?: boolean}) => {
  const Comp = asChild ? Slot : "div"

  return (
    <Comp className={cn("flex items-center gap-2", className)}>{children}</Comp>
  )
}
