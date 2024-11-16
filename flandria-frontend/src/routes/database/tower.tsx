import {gqlClient} from "@/lib/graphql-client"
import {queryClient} from "@/lib/react-query-client"

import {monsterGradeToString} from "@/utils/format-helpers"

import {graphql} from "@/gql"

import {GridItem} from "@/components/grid-item"
import {
  PageHeader,
  PageHeaderBreadcrumbs,
  PageTitle,
} from "@/components/page-header"
import {Separator} from "@/components/ui/separator"

import {queryOptions, useSuspenseQuery} from "@tanstack/react-query"
import {createFileRoute} from "@tanstack/react-router"

const query = graphql(`
  query TowerFloors {
    all_tower_floors(limit: -1) {
      items {
        floor_number
        time
        monsters {
          amount
          monster {
            code
            name
            icon
            level
            grade
          }
        }
      }
    }
  }
`)

const queryOptions_ = queryOptions({
  queryKey: ["all"],
  queryFn: async () => gqlClient.request(query),
})

export const Route = createFileRoute("/database/tower")({
  component: RouteComponent,
  loader: () => queryClient.ensureQueryData(queryOptions_),
})

function RouteComponent() {
  const {
    data: {
      all_tower_floors: {items},
    },
  } = useSuspenseQuery(queryOptions_)

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs
          items={[
            {
              label: "Home",
              href: "/",
            },
            {
              label: "Database",
              href: "/database",
            },
            {
              label: "Gilles de Rais Towers",
              href: "/database/tower",
            },
          ]}
        />
        <PageTitle title={"Gilles de Rais Towers"} />
      </PageHeader>
      <div className="grid grid-cols-12 gap-y-2 lg:mx-4">
        {items.map((towerFloor, i) => (
          <>
            {i >= 1 && <Separator className="col-span-12" />}

            <div className="col-span-12 mb-4 flex h-full lg:col-span-2 lg:mb-0 xl:col-span-1">
              <div className="flex grow flex-col items-center justify-center">
                <h2 className="whitespace-nowrap text-lg font-bold tracking-tight">
                  Floor {towerFloor.floor_number + 1}
                </h2>
                <span className="text-sm text-foreground/70">
                  {towerFloor.time}s
                </span>
              </div>
              <Separator
                orientation="vertical"
                className="mx-4 hidden lg:block"
              />
            </div>

            <div className="col-span-12 grid gap-x-6 gap-y-4 sm:grid-cols-2 md:grid-cols-3 lg:col-span-10 lg:grid-cols-4 xl:col-span-11 2xl:grid-cols-5">
              {towerFloor.monsters.map((towerFloorMonster) => (
                <GridItem.Item
                  key={`${towerFloorMonster.monster.code}-${towerFloor.floor_number}`}
                  to={`/database/monster/${towerFloorMonster.monster.code}`}
                >
                  <GridItem.Icon
                    iconName={towerFloorMonster.monster.icon}
                    actorGrade={towerFloorMonster.monster.grade}
                  />
                  <GridItem.Details>
                    <GridItem.Name>
                      {towerFloorMonster.monster.name} (
                      {towerFloorMonster.amount}x)
                    </GridItem.Name>
                    <GridItem.Subs
                      subs={[
                        `Lv. ${towerFloorMonster.monster.level}`,
                        monsterGradeToString(towerFloorMonster.monster.grade),
                      ]}
                    />
                  </GridItem.Details>
                </GridItem.Item>
              ))}
            </div>
          </>
        ))}
      </div>
    </>
  )
}
