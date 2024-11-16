import {gqlClient} from "@/lib/graphql-client"
import {queryClient} from "@/lib/react-query-client"

import {nameWithDuration} from "@/utils/format-helpers"

import {graphql} from "@/gql"

import {ColsWrapper} from "@/components/cols-wrapper"
import {AvailableFromQuestCards} from "@/components/detailed-cards/available-from-quest-card"
import {DetailsCard} from "@/components/detailed-cards/details-card"
import {getBaseMixinDetails} from "@/components/detailed-cards/helpers"
import {SkillCard} from "@/components/detailed-cards/skills-card"
import {SoldByNPCCard} from "@/components/detailed-cards/sold-by-npc-card"
import {ItemIcon} from "@/components/grid-item/ItemIcon"
import {
  PageHeader,
  PageHeaderBreadcrumbs,
  PageTitle,
} from "@/components/page-header"

import {skillBookBreadcrumbItems} from "@/routes/database/(more)/skill_book"
import {queryOptions, useSuspenseQuery} from "@tanstack/react-query"
import {createFileRoute, notFound} from "@tanstack/react-router"
import {useMemo} from "react"

const skillBookDetailedDocument = graphql(`
  query SkillBookDetailed($code: String!) {
    skill_book(code: $code) {
      ...ItemBase
      skill {
        ...SkillsCard_Fragment
      }
    }

    sold_by_npc(code: $code) {
      ...SoldByNPC
    }

    available_as_quest_reward(code: $code) {
      ...QuestsList_Fragment
    }
  }
`)

const makeQueryOptions = (code: string) =>
  queryOptions({
    queryKey: ["skillBook", code],
    queryFn: async () => gqlClient.request(skillBookDetailedDocument, {code}),
  })

export const Route = createFileRoute("/database/(more)/skill_book/$code")({
  loader: ({params: {code}}) =>
    queryClient.ensureQueryData(makeQueryOptions(code)).then((resp) => {
      if (!resp.skill_book) throw notFound()
    }),
  component: RouteComponent,
})

function RouteComponent() {
  const {code} = Route.useParams()
  const {
    data: {skill_book, sold_by_npc, available_as_quest_reward},
  } = useSuspenseQuery(makeQueryOptions(code))
  if (!skill_book) throw notFound()

  const details = useMemo(
    () => [...getBaseMixinDetails(skill_book)],
    [skill_book],
  )

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs
          items={[
            ...skillBookBreadcrumbItems,
            {label: skill_book.name, href: Route.fullPath},
          ]}
        />
        <PageTitle
          left={
            <ItemIcon
              variant="no-hover"
              iconName={skill_book.icon}
              itemGrade={skill_book.grade}
            />
          }
          title={nameWithDuration(skill_book.name, skill_book.duration)}
        />
      </PageHeader>

      <ColsWrapper>
        <div>
          <DetailsCard details={details} />
        </div>
        <div>
          <SkillCard skill={skill_book.skill} extended />
        </div>
        <div>
          <SoldByNPCCard npcs={sold_by_npc} />
          <AvailableFromQuestCards quests={available_as_quest_reward} />
        </div>
      </ColsWrapper>
    </>
  )
}
