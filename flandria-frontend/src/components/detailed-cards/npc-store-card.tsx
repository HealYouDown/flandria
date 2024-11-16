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

type NPCStoreCardProps = {
  storeItems: NpcStoreItemlist_FragmentFragment[]
}

type Section = {
  label: string
  pages: Page[]
}

type Page = {
  label: string
  items: CardItemlistItem[]
}

export function NPCStoreCard({storeItems}: NPCStoreCardProps) {
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
      page = {label: current.page_name, items: []}
      section.pages.push(page)
    }
    page.items.push(current.item)

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
                        {page.items.map((item) => (
                          <CardItemlistItem key={item.code} item={item} />
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
        <CardTitle>Shop</CardTitle>
      </CardHeader>
      {body}
    </Card>
  )
}
