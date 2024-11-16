import {cn} from "@/lib/utils"

import {isAprilFools} from "@/utils/date-helpers"

import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb"
import {Separator} from "@/components/ui/separator"

import {Link, LinkProps} from "@tanstack/react-router"
import {Fragment} from "react"
import {useDocumentTitle} from "usehooks-ts"

type PageTitleProps = {
  left?: JSX.Element
  title: string
}

export function PageTitle({title, left = undefined}: PageTitleProps) {
  useDocumentTitle(`${title} | Flandria`)

  const isFirstApril = isAprilFools()
  const headerStyle = "text-3xl font-bold tracking-tight"

  return (
    <div className="flex items-center space-x-2">
      {left}
      <h1
        className={`${headerStyle} ${isFirstApril ? "line-through decoration-red-600 decoration-4" : ""}`}
      >
        {title}
      </h1>
      {isFirstApril && <span className={headerStyle}>Stardusts</span>}
    </div>
  )
}

export type BreadcrumbItem = {
  label: string
  href: LinkProps["to"]
}

type PageHeaderBreadcrumbsProps = {
  items: BreadcrumbItem[]
}

// just to save some typing :)
export const homeBreadcrumbItems: BreadcrumbItem[] = [
  {
    label: "Home",
    href: "/",
  },
]
export const databaseBreadcrumbItems: BreadcrumbItem[] = [
  ...homeBreadcrumbItems,
  {
    label: "Database",
    href: "/database",
  },
]

export function PageHeaderBreadcrumbs({items}: PageHeaderBreadcrumbsProps) {
  return (
    <Breadcrumb>
      <BreadcrumbList>
        {items.map((item, i) => (
          <Fragment key={item.href}>
            {i >= 1 && <BreadcrumbSeparator />}
            <BreadcrumbItem key={item.href}>
              <BreadcrumbLink asChild>
                <Link to={item.href}>{item.label}</Link>
              </BreadcrumbLink>
            </BreadcrumbItem>
          </Fragment>
        ))}
      </BreadcrumbList>
    </Breadcrumb>
  )
}

export function PageHeader({className, children}: React.ComponentProps<"div">) {
  return (
    <div className={cn("flex flex-col gap-2", className)}>
      {children}
      <Separator className="mb-4" />
    </div>
  )
}
