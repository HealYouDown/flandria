import {cn} from "@/lib/utils"

import {ScrollArea} from "@/components/ui/scroll-area"

import {Slot} from "@radix-ui/react-slot"
import {createLink} from "@tanstack/react-router"
import * as React from "react"

const Card = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({className, ...props}, ref) => (
  <div
    ref={ref}
    className={cn(
      "rounded-lg border bg-card text-card-foreground shadow-sm",
      className,
    )}
    {...props}
  />
))
Card.displayName = "Card"

const CardHeader = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({className, ...props}, ref) => (
  <div
    ref={ref}
    className={cn("flex flex-col space-y-1.5 border-b px-6 py-4", className)}
    {...props}
  />
))
CardHeader.displayName = "CardHeader"

const CardTitle = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLHeadingElement>
>(({className, ...props}, ref) => (
  <h2
    ref={ref}
    className={cn(
      "text-2xl font-semibold leading-none tracking-tight",
      className,
    )}
    {...props}
  />
))
CardTitle.displayName = "CardTitle"

const CardDescription = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({className, ...props}, ref) => (
  <p
    ref={ref}
    className={cn("text-sm text-muted-foreground", className)}
    {...props}
  />
))
CardDescription.displayName = "CardDescription"

const CardContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({className, ...props}, ref) => (
  <div ref={ref} className={cn("px-6 py-4", className)} {...props} />
))
CardContent.displayName = "CardContent"

const CardFooter = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({className, ...props}, ref) => (
  <div
    ref={ref}
    className={cn("flex items-center p-6", className)}
    {...props}
  />
))
CardFooter.displayName = "CardFooter"

// the following components are added by us for our detailed lists etc.

const CardContentList = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({className, ...props}, ref) => (
  <div ref={ref} className={cn(className)} {...props} />
))
CardContent.displayName = "CardContentList"

const CardContentScrollList = ({
  children,
  className,
  ...props
}: React.ComponentProps<typeof ScrollArea>) => (
  <ScrollArea className={cn(className)} {...props}>
    {children}
  </ScrollArea>
)
CardContentScrollList.displayName = "CardContentScrollList"

const CardContentListItem = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & {asChild?: boolean}
>(({className, asChild = false, ...props}, ref) => {
  const Comp = asChild ? Slot : "div"

  return (
    <Comp
      ref={ref}
      className={cn(
        "block w-full px-6 py-3 [&:not(:last-child)]:border-b",
        className,
      )}
      {...props}
    />
  )
})
CardContentListItem.displayName = "CardContentListItem"

interface CardContentLinkListItemProps
  extends React.AnchorHTMLAttributes<HTMLAnchorElement> {}

const CardContentLinkListItem_ = React.forwardRef<
  HTMLAnchorElement,
  CardContentLinkListItemProps
>(({className, children, ...props}, ref) => (
  <CardContentListItem
    asChild
    className={cn(
      "last:rounded-b-md hover:bg-accent hover:text-accent-foreground",
      className,
    )}
  >
    <a ref={ref} {...props}>
      {children}
    </a>
  </CardContentListItem>
))
CardContentLinkListItem_.displayName = "CardContentLinkListItem"
const CardContentLinkListItem = createLink(CardContentLinkListItem_)

export {
  Card,
  CardHeader,
  CardFooter,
  CardTitle,
  CardDescription,
  CardContent,
  CardContentList,
  CardContentScrollList,
  CardContentListItem,
  CardContentLinkListItem,
}
