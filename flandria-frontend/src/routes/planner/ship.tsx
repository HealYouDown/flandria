import {BaseClassType} from "@/lib/enums"
import {queryClient} from "@/lib/react-query-client"

import {
  PageHeader,
  PageHeaderBreadcrumbs,
  PageTitle,
  homeBreadcrumbItems,
} from "@/components/page-header"
import {
  getAvailableSkillPointsSea,
  groupSkillsData,
} from "@/components/planner/skill-helpers"
import {SkillPlannerCard} from "@/components/planner/skill-planner-card"

import {seaLevelOptions} from "@/routes/planner/-combobox-options"
import {makePlannerQueryOptions} from "@/routes/planner/-query"
import {
  SHIP_SKILL_CODES,
  SHIP_SKILL_POSITIONS,
} from "@/routes/planner/-skill-codes"
import {useSuspenseQuery} from "@tanstack/react-query"
import {createFileRoute} from "@tanstack/react-router"

export const Route = createFileRoute("/planner/ship")({
  loader: () =>
    queryClient.ensureQueryData(
      makePlannerQueryOptions(BaseClassType.Ship, SHIP_SKILL_CODES),
    ),
  component: RouteComponent,
})

function RouteComponent() {
  const {
    data: {
      all_player_skills: {skills},
    },
  } = useSuspenseQuery(
    makePlannerQueryOptions(BaseClassType.Ship, SHIP_SKILL_CODES),
  )

  const groupedSkillData = groupSkillsData(skills)

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs
          items={[
            ...homeBreadcrumbItems,
            {label: "Planner Ship", href: "/planner/ship"},
          ]}
        />
        <PageTitle title="Ship" />
      </PageHeader>
      <div>
        <SkillPlannerCard
          skillData={groupedSkillData}
          positions={SHIP_SKILL_POSITIONS}
          background="ship"
          alwaysAllowedClasses={[
            "is_torpedo",
            "is_armored",
            "is_assault",
            "is_big_gun",
            "is_maintenance",
          ]}
          classOptions={null}
          levelOptions={seaLevelOptions}
          getAvailableSkillPointsFromLevel={getAvailableSkillPointsSea}
        />
      </div>
    </>
  )
}
