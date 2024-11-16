import {cn} from "@/lib/utils"

import {isAprilFools} from "@/utils/date-helpers"

import {MobileNavMenu} from "@/components/mobile-nav-menu"
import {ThemeToggleButton} from "@/components/theme-toggle-button"
import {Button} from "@/components/ui/button"
import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuTrigger,
  navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu"

import {GlobalSearchBar} from "./global-search-bar"

import {GitHubLogoIcon} from "@radix-ui/react-icons"
import {Link, LinkProps} from "@tanstack/react-router"
import {AnchorIcon} from "lucide-react"
import * as React from "react"

export type NavListLink = {
  title: string
  href: LinkProps["to"]
  description?: string
}

export type NavListExternalLink = {
  title: string
  href: string
  description?: string
}

export const plannerLinks: NavListLink[] = [
  {
    title: "Explorer",
    href: "/planner/explorer",
    description: "Nimble fighters wielding pistols, rifles, and clever traps.",
  },
  {
    title: "Saint",
    href: "/planner/saint",
    description:
      "Nature's chosen, harnessing the light's blessing and darkness's wrath.",
  },
  {
    title: "Noble",
    href: "/planner/noble",
    description:
      "Elemental sorcerers who command powerful magic to control and devastate.",
  },
  {
    title: "Mercenary",
    href: "/planner/mercenary",
    description: "Unbreakable warriors with unmatched defensive skills.",
  },
  {
    title: "Ship",
    href: "/planner/ship",
    description:
      "Your essential vessel for island travel and a shield against monsters and pirates.",
  },
]

export const moreLinks: NavListLink[] = [
  {
    title: "Maps",
    href: "/database/map",
    description: " The vast, explorable areas of the game.",
  },
  {
    title: "NPCs",
    href: "/database/npc",
    description: "All lively residents of Florensia.",
  },
  {
    title: "Gilles de Rais Towers",
    href: "/database/tower",
    description: "A 100-floor dungeon packed with monsters and treasure.",
  },
]

export const downloadLinks: NavListExternalLink[] = [
  {
    title: "Essence Guide (EN)",
    href: "/files/essence_guide_en.pdf",
    description: "Essence Guide in English.",
  },
  {
    title: "Essence Guide (DE)",
    href: "/files/essence_guide_de.pdf",
    description: "Essence Guide in German.",
  },
  {
    title: "Combat Pet Stats",
    href: "/files/pet_stats.pdf",
    description: "A list of S+ stats per pevel for all pets.",
  },
]

export const HeaderIcon = () => {
  if (isAprilFools()) {
    return (
      <Link className="shrink-0" to="/">
        <img
          className="h-12 w-12 animate-[spin_2s_linear_infinite] rounded-full"
          src="/assets/icons/ieu_137.png"
        />
      </Link>
    )
  }

  return (
    <Link className="shrink-0" to="/">
      <img className="h-12 w-auto" src="/logo.png" />
    </Link>
  )
}

export function NavMenu() {
  return (
    <header className="sticky top-0 z-50 flex items-center gap-x-4 bg-background/70 px-4 py-2 backdrop-blur-sm md:px-6">
      <MobileNavMenu />

      <HeaderIcon />

      <NavigationMenu className="hidden md:block">
        <NavigationMenuList>
          <NavigationMenuItem>
            <NavigationMenuLink
              asChild
              className={navigationMenuTriggerStyle()}
            >
              <Link to="/database/monster">Monsters</Link>
            </NavigationMenuLink>
          </NavigationMenuItem>

          <NavigationMenuItem>
            <NavigationMenuLink
              asChild
              className={navigationMenuTriggerStyle()}
            >
              <Link to="/database">Database</Link>
            </NavigationMenuLink>
          </NavigationMenuItem>

          <NavigationMenuItem>
            <NavigationMenuLink
              asChild
              className={navigationMenuTriggerStyle()}
            >
              <Link to="/database/quest">Quests</Link>
            </NavigationMenuLink>
          </NavigationMenuItem>

          <NavigationMenuItem>
            <NavigationMenuTrigger>Planner</NavigationMenuTrigger>
            <NavigationMenuContent>
              <ListItemWrapper>
                {plannerLinks.map((linkItem) => (
                  <ListItem
                    key={linkItem.href}
                    title={linkItem.title}
                    href={linkItem.href}
                  >
                    {linkItem.description}
                  </ListItem>
                ))}
              </ListItemWrapper>
            </NavigationMenuContent>
          </NavigationMenuItem>

          <NavigationMenuItem>
            <NavigationMenuTrigger>More</NavigationMenuTrigger>
            <NavigationMenuContent>
              <ListItemWrapper>
                {moreLinks.map((linkItem) => (
                  <ListItem
                    key={linkItem.href}
                    title={linkItem.title}
                    href={linkItem.href}
                  >
                    {linkItem.description}
                  </ListItem>
                ))}
              </ListItemWrapper>
            </NavigationMenuContent>
          </NavigationMenuItem>

          <NavigationMenuItem>
            <NavigationMenuTrigger>Downloads</NavigationMenuTrigger>
            <NavigationMenuContent>
              <ListItemWrapper>
                {downloadLinks.map((linkItem) => (
                  <ExternalLinkItem
                    key={linkItem.href}
                    title={linkItem.title}
                    href={linkItem.href}
                  >
                    {linkItem.description}
                  </ExternalLinkItem>
                ))}
              </ListItemWrapper>
            </NavigationMenuContent>
          </NavigationMenuItem>
        </NavigationMenuList>
      </NavigationMenu>

      <div className="grow" />
      <GlobalSearchBar className="hidden max-w-[800px] lg:mx-4 lg:flex xl:mx-6 2xl:mx-10" />
      <div className="grow" />

      <div className="flex items-center gap-0.5">
        <Button variant="ghost" size="icon" asChild>
          <a target="_blank" href="https://florensia-online.com">
            <AnchorIcon className="icon-size" />
          </a>
        </Button>
        <Button variant="ghost" size="icon" asChild>
          <a target="_blank" href="https://github.com/HealYouDown/flandria">
            <GitHubLogoIcon className="icon-size" />
          </a>
        </Button>
        <ThemeToggleButton />
      </div>
    </header>
  )
}

const ListItemWrapper = (props: React.PropsWithChildren) => (
  <ul className="z-50 grid w-[400px] gap-3 p-4 md:w-[500px] md:grid-cols-2 lg:w-[600px]">
    {props.children}
  </ul>
)

const ListItem = React.forwardRef<
  React.ElementRef<"a">,
  React.ComponentPropsWithoutRef<"a">
>(({className, title, href, children, ...props}, ref) => {
  return (
    <li>
      <NavigationMenuLink asChild>
        <Link
          ref={ref}
          to={href}
          className={cn(
            "block select-none space-y-1 rounded-md p-3 leading-none no-underline outline-none transition-colors hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground",
            className,
          )}
          {...props}
        >
          <div className="text-sm font-bold leading-none">{title}</div>
          <p className="line-clamp-2 text-sm leading-snug text-muted-foreground">
            {children}
          </p>
        </Link>
      </NavigationMenuLink>
    </li>
  )
})

const ExternalLinkItem = React.forwardRef<
  React.ElementRef<"a">,
  React.ComponentPropsWithoutRef<"a">
>(({className, title, href, children, ...props}, ref) => {
  return (
    <li>
      <NavigationMenuLink asChild>
        <a
          target="_blank"
          ref={ref}
          href={href}
          className={cn(
            "block select-none space-y-1 rounded-md p-3 leading-none no-underline outline-none transition-colors hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground",
            className,
          )}
          {...props}
        >
          <div className="text-sm font-bold leading-none">{title}</div>
          <p className="line-clamp-2 text-sm leading-snug text-muted-foreground">
            {children}
          </p>
        </a>
      </NavigationMenuLink>
    </li>
  )
})
