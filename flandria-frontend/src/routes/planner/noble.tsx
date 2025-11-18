import {queryClient} from "@/lib/react-query-client"

import {BaseClassType} from "@/gql/graphql"

import {
  PageHeader,
  PageHeaderBreadcrumbs,
  PageTitle,
  homeBreadcrumbItems,
} from "@/components/page-header"
import {
  getAvailableSkillPointsLand,
  groupSkillsData,
} from "@/components/planner/skill-helpers"
import {SkillPlannerCard} from "@/components/planner/skill-planner-card"
import {StatsPlannerCard} from "@/components/planner/stats-planner-card"

import {
  landLevelOptions,
  nobleClassOptions,
} from "@/routes/planner/-combobox-options"
import {makePlannerQueryOptions} from "@/routes/planner/-query"
import {
  NOBLE_SKILL_CODES,
  NOBLE_SKILL_POSITIONS,
} from "@/routes/planner/-skill-codes"
import {useSuspenseQuery} from "@tanstack/react-query"
import {createFileRoute} from "@tanstack/react-router"

export const Route = createFileRoute("/planner/noble")({
  loader: () =>
    queryClient.ensureQueryData(
      makePlannerQueryOptions(BaseClassType.Noble, NOBLE_SKILL_CODES),
    ),
  component: RouteComponent,
})

function RouteComponent() {
  const {
    data: {
      all_player_skills: {skills},
    },
  } = useSuspenseQuery(
    makePlannerQueryOptions(BaseClassType.Noble, NOBLE_SKILL_CODES),
  )

  const groupedSkillData = groupSkillsData(skills)

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs
          items={[
            ...homeBreadcrumbItems,
            {label: "Planner Noble", href: "/planner/noble"},
          ]}
        />
        <PageTitle title="Noble" />
      </PageHeader>
      <div className="flex flex-col items-center justify-around gap-10 lg:flex-row lg:items-start">
        <SkillPlannerCard
          skillData={groupedSkillData}
          positions={NOBLE_SKILL_POSITIONS}
          background="noble"
          alwaysAllowedClasses={["is_noble"]}
          classOptions={nobleClassOptions}
          levelOptions={landLevelOptions}
          getAvailableSkillPointsFromLevel={getAvailableSkillPointsLand}
        />
        <StatsPlannerCard baseClass={BaseClassType.Noble} />
      </div>
    </>
  )
}
