import {gqlClient} from "@/lib/graphql-client"
import {cn} from "@/lib/utils"

import {
  characterClassStringFromObject,
  genderToString,
  monsterGradeToString,
  shipClassFromObject,
} from "@/utils/format-helpers"
import {getLinkFromTablename} from "@/utils/utils"

import {graphql} from "@/gql"
import {GlobalSearchQuery} from "@/gql/graphql"

import {GridItem} from "@/components/grid-item"
import {Popover, PopoverContent, PopoverTrigger} from "@/components/ui/popover"
import {Spinner} from "@/components/ui/spinner"

import {Separator} from "./ui/separator"

import {useQuery} from "@tanstack/react-query"
import {SearchIcon} from "lucide-react"
import {useRef} from "react"
import * as React from "react"
import {useDebounceValue, useOnClickOutside} from "usehooks-ts"

const query = graphql(`
  query GlobalSearch($s: String!) {
    search(s: $s, limit: 15) {
      __typename
      ... on ActorMixin {
        code
        name
        icon
        actorGrade: grade
        level
        is_sea
      }
      ... on ItemList {
        code
        name
        icon
        tablename
        duration
        gender
        level_land
        level_sea
        itemGrade: grade
        # ...EffectsFragment
        ...CharacterClassFragment
        ...ShipClassFragment
      }
      ... on Quest {
        code
        title
        level
        is_sea
      }
    }
  }
`)

const MIN_SEARCH_INPUT_LENGTH = 2

type SearchResultProps = {
  data: GlobalSearchQuery
  closePopup: () => void
}

function SearchResults({data: {search}, closePopup}: SearchResultProps) {
  const gridItemClassName =
    "rounded-lg transition-colors duration-200 !animate-none hover:bg-accent px-1"

  const monsterItems = search
    .filter((obj) => obj.__typename === "Monster")
    .map((monster) => (
      <GridItem.Item
        key={monster.code}
        className={gridItemClassName}
        to="/database/monster/$code"
        params={{code: monster.code}}
        onClick={closePopup}
      >
        <GridItem.Icon
          size="medium"
          iconName={monster.icon}
          actorGrade={monster.actorGrade}
        />
        <GridItem.Details>
          <GridItem.Name>{monster.name}</GridItem.Name>
          <GridItem.Subs
            subs={[
              `Lv. ${monster.level}`,
              monsterGradeToString(monster.actorGrade),
              monster.is_sea ? "Sea" : "Land",
            ]}
          />
        </GridItem.Details>
      </GridItem.Item>
    ))

  const npcItems = search
    .filter((obj) => obj.__typename === "Npc")
    .map((npc) => (
      <GridItem.Item
        key={npc.code}
        onClick={closePopup}
        className={gridItemClassName}
        to="/database/npc/$code"
        params={{code: npc.code}}
      >
        <GridItem.Icon
          size="medium"
          iconName={npc.icon}
          actorGrade={npc.actorGrade}
        />
        <GridItem.Details>
          <GridItem.Name>{npc.name}</GridItem.Name>
          <GridItem.Subs
            subs={[`Lv. ${npc.level}`, npc.is_sea ? "Sea" : "Land"]}
          />
        </GridItem.Details>
      </GridItem.Item>
    ))

  const items = search
    .filter((obj) => obj.__typename === "ItemList")
    .map((item) => {
      const subs = []
      if (item.level_land !== null && item.level_sea === null) {
        subs.push(`Land Lv. ${item.level_land}`)
      } else if (item.level_land === null && item.level_sea !== null) {
        subs.push(`Sea Lv. ${item.level_sea}`)
      } else if (item.level_land !== null && item.level_sea !== null) {
        subs.push(`Lv. ${item.level_land}/${item.level_sea}`)
      }

      if (item.gender) {
        subs.push(genderToString(item.gender))
      }
      subs.push(characterClassStringFromObject(item))
      subs.push(shipClassFromObject(item))

      return (
        <GridItem.Item
          key={item.code}
          onClick={closePopup}
          className={gridItemClassName}
          to={getLinkFromTablename(item.tablename)}
          params={{code: item.code}}
        >
          <GridItem.Icon
            size="medium"
            iconName={item.icon}
            itemGrade={item.itemGrade}
          />
          <GridItem.Details>
            <GridItem.Name duration={item.duration}>{item.name}</GridItem.Name>
            <GridItem.Subs subs={subs} />
            {/* <GridItem.Effects effects={item.effects || []} /> */}
          </GridItem.Details>
        </GridItem.Item>
      )
    })

  const questItems = search
    .filter((obj) => obj.__typename === "Quest")
    .map((quest) => (
      <GridItem.Item
        key={quest.code}
        onClick={closePopup}
        className={gridItemClassName}
        to="/database/quest/$code"
        params={{code: quest.code}}
      >
        <GridItem.Details>
          <GridItem.Name>{quest.title}</GridItem.Name>
          <GridItem.Subs
            subs={[`Lv. ${quest.level}`, quest.is_sea ? "Sea" : "Land"]}
          />
        </GridItem.Details>
      </GridItem.Item>
    ))

  const sections = []
  if (monsterItems.length > 0)
    sections.push({label: "Monsters", items: monsterItems})
  if (npcItems.length > 0) sections.push({label: "NPCs", items: npcItems})
  if (items.length > 0) sections.push({label: "Items", items: items})
  if (questItems.length > 0) sections.push({label: "Quests", items: questItems})

  return (
    <div className="flex flex-col">
      {sections.map((section, i) => (
        <React.Fragment key={section.label}>
          {i >= 1 && <Separator className="my-1" />}
          <h2 className="font-bold tracking-tight">{section.label}</h2>
          <div className="grid grid-cols-1 gap-x-3 gap-y-2 py-2 xl:grid-cols-2 2xl:grid-cols-3">
            {section.items}
          </div>
        </React.Fragment>
      ))}
    </div>
  )
}

interface GlobalSearchBarProps {
  className?: string
}

export function GlobalSearchBar({className}: GlobalSearchBarProps) {
  const [debouncedSearchValue, setSearchValue] = useDebounceValue("", 500)
  const [hasFocus, setHasFocus] = React.useState(false)

  const contentRef = useRef(null)
  const searchbarRef = useRef(null)

  const {data, isFetching} = useQuery({
    queryKey: ["globalSearch", debouncedSearchValue],
    queryFn: async () => gqlClient.request(query, {s: debouncedSearchValue}),
    enabled: debouncedSearchValue.length >= MIN_SEARCH_INPUT_LENGTH,
    placeholderData: (prev) => prev,
    gcTime: 0,
    staleTime: 0,
  })

  const onSearchbarFocus = () => {
    setHasFocus(true)
  }
  useOnClickOutside([contentRef, searchbarRef], () => setHasFocus(false))

  const hasResults = (data?.search.length || 0) > 0

  return (
    <Popover
      open={
        hasFocus &&
        hasResults &&
        debouncedSearchValue.length >= MIN_SEARCH_INPUT_LENGTH
      }
    >
      <PopoverTrigger asChild>
        <div
          ref={searchbarRef}
          className={cn(
            "flex h-10 w-full flex-nowrap items-center gap-2 rounded-md border border-input bg-none px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground has-[:focus-visible]:outline-none has-[:focus-visible]:ring-2 has-[:focus-visible]:ring-ring has-[:focus-visible]:ring-offset-2",
            className,
          )}
        >
          {isFetching ? (
            <Spinner className="h-[1.2rem] w-[1rem]" />
          ) : (
            <SearchIcon className="h-[1.2rem] w-[1rem]" />
          )}
          <input
            className="w-full border-none bg-transparent shadow-none outline-none"
            type="search"
            onChange={(event) => setSearchValue(event.target.value)}
            onFocus={onSearchbarFocus}
          />
        </div>
      </PopoverTrigger>
      <PopoverContent
        ref={contentRef}
        onOpenAutoFocus={(e) => e.preventDefault()}
        className="popover-content-width-full mt-1 max-h-[400px] overflow-y-scroll"
      >
        {data && (
          <SearchResults data={data} closePopup={() => setHasFocus(false)} />
        )}
      </PopoverContent>
    </Popover>
  )
}
