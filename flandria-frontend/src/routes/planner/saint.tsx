import {BaseClassType} from "@/lib/enums"
import {queryClient} from "@/lib/react-query-client"

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
  saintClassOptions,
} from "@/routes/planner/-combobox-options"
import {makePlannerQueryOptions} from "@/routes/planner/-query"
import {
  SAINT_SKILLS_POSITIONS,
  SAINT_SKILL_CODES,
} from "@/routes/planner/-skill-codes"
import {useSuspenseQuery} from "@tanstack/react-query"
import {createFileRoute} from "@tanstack/react-router"

export const Route = createFileRoute("/planner/saint")({
  loader: () =>
    queryClient.ensureQueryData(
      makePlannerQueryOptions(BaseClassType.Saint, SAINT_SKILL_CODES),
    ),
  component: RouteComponent,
})

function RouteComponent() {
  const {
    data: {
      all_player_skills: {skills},
    },
  } = useSuspenseQuery(
    makePlannerQueryOptions(BaseClassType.Saint, SAINT_SKILL_CODES),
  )

  const groupedSkillData = groupSkillsData(skills)

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs
          items={[
            ...homeBreadcrumbItems,
            {label: "Planner Saint", href: "/planner/saint"},
          ]}
        />
        <PageTitle title="Saint" />
      </PageHeader>
      <div className="flex flex-col items-center justify-around gap-10 lg:flex-row lg:items-start">
        <SkillPlannerCard
          skillData={groupedSkillData}
          positions={SAINT_SKILLS_POSITIONS}
          background="saint"
          alwaysAllowedClasses={["is_saint"]}
          classOptions={saintClassOptions}
          levelOptions={landLevelOptions}
          getAvailableSkillPointsFromLevel={getAvailableSkillPointsLand}
        />
        <StatsPlannerCard baseClass={BaseClassType.Saint} />
      </div>
    </>
  )
}
