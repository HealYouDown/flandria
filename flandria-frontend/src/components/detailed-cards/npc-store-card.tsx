import {graphql} from "@/gql"
import {NpcStoreItemlist_FragmentFragment} from "@/gql/graphql"

import {CardItemlistItem} from "@/components/detailed-cards/helpers"
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion"
import {
  Card,
  CardContent,
  CardContentScrollList,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

graphql(`
  fragment NPCStoreItemlist_Fragment on NpcStoreItem {
    section_name
    page_name
    item {
      ...Card_ItemlistItem
    }
  }
`)

export type NPCStoreEntry = Pick<
  NpcStoreItemlist_FragmentFragment,
  "section_name" | "page_name" | "item"
> & {
  // e.g. the exchange cost
  subs?: string[]
}

type NPCStoreCardProps = {
  storeItems: NPCStoreEntry[]
  title?: string
  hideIfEmpty?: boolean
}

type Section = {
  label: string
  pages: Page[]
}

type Page = {
  label: string
  entries: NPCStoreEntry[]
}

export function NPCStoreCard({
  storeItems,
  title = "Shop",
  hideIfEmpty = false,
}: NPCStoreCardProps) {
  if (hideIfEmpty && storeItems.length === 0) return null

  let body = (
    <CardContent>
      <p>No items sold.</p>
    </CardContent>
  )

  const sections = storeItems.reduce<Section[]>((sections, current) => {
    let section = sections.find((s) => s.label === current.section_name)
    if (!section) {
      section = {label: current.section_name, pages: []}
      sections.push(section)
    }

    let page = section.pages.find((p) => p.label === current.page_name)
    if (!page) {
      page = {label: current.page_name, entries: []}
      section.pages.push(page)
    }
    page.entries.push(current)

    return sections
  }, [])

  if (sections.length > 0) {
    body = (
      <CardContentScrollList className="px-6">
        <Accordion type="single" className="w-full" collapsible>
          {sections.map((section) => (
            <AccordionItem
              key={section.label}
              className="last:border-none"
              value={section.label}
            >
              <AccordionTrigger className="py-3 font-bold tracking-tight">
                {section.label}
              </AccordionTrigger>
              <AccordionContent className="pb-0 pl-2">
                <Accordion type="single" collapsible>
                  {section.pages.map((page) => (
                    <AccordionItem
                      key={page.label}
                      className="last:border-none"
                      value={page.label}
                    >
                      <AccordionTrigger>{page.label}</AccordionTrigger>
                      <AccordionContent className="pb-0">
                        {page.entries.map((entry, idx) => (
                          <CardItemlistItem
                            key={idx}
                            item={entry.item}
                            additionalSubs={entry.subs}
                          />
                        ))}
                      </AccordionContent>
                    </AccordionItem>
                  ))}
                </Accordion>
              </AccordionContent>
            </AccordionItem>
          ))}
        </Accordion>
      </CardContentScrollList>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      {body}
    </Card>
  )
}
