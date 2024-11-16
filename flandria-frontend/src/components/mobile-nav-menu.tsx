import {cn} from "@/lib/utils"

import {
  NavListExternalLink,
  NavListLink,
  downloadLinks,
  moreLinks,
  plannerLinks,
} from "@/components/nav-menu"
import {Button} from "@/components/ui/button"
import {Separator} from "@/components/ui/separator"
import {Sheet, SheetContent, SheetTrigger} from "@/components/ui/sheet"

import {HamburgerMenuIcon} from "@radix-ui/react-icons"
import {Link} from "@tanstack/react-router"
import * as React from "react"

interface MenuLinkProps {
  title: string
  href: string | NavListLink["href"]
  description?: string
  className?: string
  closeHandler: () => void
}

const MenuLink = ({title, href, closeHandler, className}: MenuLinkProps) => (
  <Link
    onClick={closeHandler}
    className={cn("font-semibold", className)}
    to={href}
  >
    {title}
  </Link>
)

const ExternalMenuLink = ({
  title,
  href,
  closeHandler,
  className,
}: MenuLinkProps) => (
  <a
    target="_blank"
    onClick={closeHandler}
    className={cn("font-semibold", className)}
    href={href}
  >
    {title}
  </a>
)

interface SectionCommonProps {
  title: string
  closeHandler: MenuLinkProps["closeHandler"]
}

interface SectionInternalProps extends SectionCommonProps {
  links: NavListLink[]
  external?: false
}

interface SectionExternalProps extends SectionCommonProps {
  links: NavListExternalLink[]
  external?: true
}

type SectionProps = SectionInternalProps | SectionExternalProps

const Section = ({
  title,
  links,
  closeHandler,
  external = false,
}: SectionProps) => {
  const Comp = external ? ExternalMenuLink : MenuLink

  return (
    <div>
      <h2 className="font-semibold">{title}</h2>
      <div className="flex flex-col space-y-1">
        {links.map((link) => (
          <Comp
            key={link.href}
            closeHandler={closeHandler}
            className="font-normal text-muted-foreground"
            {...link}
          />
        ))}
      </div>
    </div>
  )
}

export function MobileNavMenu() {
  const [open, setOpen] = React.useState(false)
  const closeHandler = () => setOpen(false)

  return (
    <Sheet open={open} onOpenChange={setOpen}>
      <SheetTrigger asChild>
        <Button
          className="mr-2 px-0 text-base hover:bg-transparent focus-visible:bg-transparent focus-visible:ring-0 focus-visible:ring-offset-0 md:hidden"
          variant="ghost"
        >
          <HamburgerMenuIcon className="h-[1.2rem] w-[1.2rem]" />
        </Button>
      </SheetTrigger>
      <SheetContent side="left">
        <div className="flex justify-center">
          <img src="/full_logo_small.png" />
        </div>
        <Separator className="my-1" />
        <nav className="flex flex-col space-y-4">
          <MenuLink
            closeHandler={closeHandler}
            title="Monsters"
            href="/database/monster"
          />
          <MenuLink
            closeHandler={closeHandler}
            title="Database"
            href="/database"
          />
          <MenuLink
            closeHandler={closeHandler}
            title="Quests"
            href="/database/quest"
          />
          <Section
            closeHandler={closeHandler}
            title="Planner"
            links={plannerLinks}
          />
          <Section closeHandler={closeHandler} title="More" links={moreLinks} />
          <Section
            closeHandler={closeHandler}
            title="Downloads"
            links={downloadLinks}
            external
          />
        </nav>
      </SheetContent>
    </Sheet>
  )
}
