import {gqlClient} from "@/lib/graphql-client"
import {queryClient} from "@/lib/react-query-client"

import {formatSeconds} from "@/utils/date-helpers"
import {
  booleanToDisplayString,
  monsterGradeToString,
  rangeToMeters,
} from "@/utils/format-helpers"

import {graphql} from "@/gql"

import {ColsWrapper} from "@/components/cols-wrapper"
import {DetailsCard} from "@/components/detailed-cards/details-card"
import {DropsListCard} from "@/components/detailed-cards/drops-list-card"
import {MapCard} from "@/components/detailed-cards/map-card"
import {ModelCard} from "@/components/detailed-cards/model-card"
import {QuestsListCard} from "@/components/detailed-cards/quests-list-card"
import {SkillCard} from "@/components/detailed-cards/skills-card"
import {ItemIcon} from "@/components/grid-item/ItemIcon"
import {
  PageHeader,
  PageHeaderBreadcrumbs,
  PageTitle,
} from "@/components/page-header"
import {Tooltip, TooltipContent, TooltipTrigger} from "@/components/ui/tooltip"

import {monsterBreadcrumbItems} from "@/routes/database/(actors)/monster"
import {queryOptions, useSuspenseQuery} from "@tanstack/react-query"
import {createFileRoute, notFound} from "@tanstack/react-router"
import {useMemo} from "react"

const monsterDetailedDocument = graphql(`
  query MonsterDetailed($code: String!) {
    monster(code: $code) {
      code
      name
      icon
      grade
      is_sea
      level
      health_points
      physical_defense
      magical_defense
      minimum_physical_damage
      maximum_physical_damage
      minimum_magical_damage
      maximum_magical_damage
      is_ranged
      attack_range
      experience
      is_tameable
      attack_vision_range
      nearby_attack_vision_range

      # TODO: definitely have to change that so it's a 1:n relationship.. :)
      skill_1 {
        ...SkillsCard_Fragment
      }
      skill_2 {
        ...SkillsCard_Fragment
      }

      models {
        ...ModelFragment
      }

      drops {
        ...DropsList_Fragment
      }

      money {
        ...DropsListMoney_Fragment
      }

      positions {
        map_code
        ...MapCanvas_MonsterPositionFragment
      }
    }

    # less data queried instead of asking for map data on each positions edge
    maps: all_maps(limit: -1, filter: {monsters: {monster_code: {eq: $code}}}) {
      items {
        ...MapCanvas_MapDetailsFragment
      }
    }

    quests: all_quests(
      limit: -1
      filter: {missions: {monster_code: {eq: $code}}}
    ) {
      items {
        ...QuestsList_Fragment
      }
    }
  }
`)

const makeQueryOptions = (code: string) =>
  queryOptions({
    queryKey: ["monster", code],
    queryFn: async () => gqlClient.request(monsterDetailedDocument, {code}),
  })

export const Route = createFileRoute("/database/(actors)/monster/$code")({
  loader: ({params: {code}}) =>
    queryClient.ensureQueryData(makeQueryOptions(code)).then((resp) => {
      if (!resp.monster) throw notFound()
    }),
  component: RouteComponent,
})

function RouteComponent() {
  const {code} = Route.useParams()
  const {
    data: {monster, maps, quests},
  } = useSuspenseQuery(makeQueryOptions(code))
  if (!monster) throw notFound()

  const respawnTimes = useMemo(
    () =>
      [...new Set(monster.positions.map((pos) => pos.respawn_time))].sort(
        (a, b) => a - b,
      ),
    [monster],
  )

  const details = useMemo(
    () => [
      {
        label: "Type",
        value: monsterGradeToString(monster.grade),
      },
      {
        label: "Area",
        value: monster.is_sea ? "Sea" : "Land",
      },
      {
        label: "Level",
        value: monster.level.toString(),
      },
      {
        label: "HP",
        value: monster.health_points.toLocaleString(),
      },
      {
        label: "Physical Defense",
        value: monster.physical_defense.toLocaleString(),
      },
      {
        label: "Magical Defense",
        value: monster.magical_defense.toLocaleString(),
      },
      {
        label: "Physical Hit",
        value: `${monster.minimum_physical_damage.toLocaleString()} ~ ${monster.maximum_physical_damage.toLocaleString()}`,
      },
      {
        label: "Magical Hit",
        value: `${monster.minimum_magical_damage.toLocaleString()} ~ ${monster.maximum_magical_damage.toLocaleString()}`,
      },
      {
        label: "Attack Range",
        value: `${monster.is_ranged ? "Range" : "Meele"}, ${rangeToMeters(monster.attack_range)}m`,
      },
      {
        label: "Experience",
        value: monster.experience.toLocaleString(),
      },
      {
        label: "Respawn",
        description: "Respawn timer(s)",
        value:
          respawnTimes.length === 0 ? (
            "None"
          ) : respawnTimes.length === 1 ? (
            formatSeconds(respawnTimes[0])
          ) : (
            <Tooltip delayDuration={50}>
              <TooltipTrigger>View list</TooltipTrigger>
              <TooltipContent>
                <ul>
                  {respawnTimes.map((time, i) => (
                    <li key={i}>{formatSeconds(time)}</li>
                  ))}
                </ul>
              </TooltipContent>
            </Tooltip>
          ),
      },
      {
        label: "Tameable",
        description:
          "Whether the Monster can be tamed using the skill Temptation",
        value: booleanToDisplayString(monster.is_tameable),
      },
      {
        label: "Vision Range",
        description:
          "The distance within which monsters will engage you in combat.",
        value: `${rangeToMeters(monster.attack_vision_range)}m`,
      },
      {
        label: "Nearby Vision Range",
        description:
          "The distance within which monsters will support nearby allies in combat.",
        value: `${rangeToMeters(monster.nearby_attack_vision_range)}m`,
      },
    ],
    [monster, respawnTimes],
  )

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs
          items={[
            ...monsterBreadcrumbItems,
            {label: monster.name, href: Route.fullPath},
          ]}
        />
        <PageTitle
          left={
            <ItemIcon
              variant="no-hover"
              iconName={monster.icon}
              actorGrade={monster.grade}
            />
          }
          title={monster.name}
        />
      </PageHeader>

      <ColsWrapper>
        <div>
          {monster.models && <ModelCard models={monster.models} />}
          <DetailsCard details={details} />
          {monster.skill_1 && (
            <SkillCard
              title="Skill 1"
              skill={monster.skill_1}
              extended={false}
            />
          )}
          {monster.skill_2 && (
            <SkillCard
              title="Skill 2"
              skill={monster.skill_2}
              extended={false}
            />
          )}
        </div>
        <div>
          <QuestsListCard quests={quests.items} />
          <MapCard
            maps={maps.items.map((map) => ({
              map,
              positions: monster.positions.filter(
                (pos) => pos.map_code === map.code,
              ),
            }))}
          />
        </div>
        <div>
          <DropsListCard money={monster.money} drops={monster.drops} />
        </div>
      </ColsWrapper>
    </>
  )
}
