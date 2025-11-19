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
  explorerClassOptions,
  landLevelOptions,
} from "@/routes/planner/-combobox-options"
import {makePlannerQueryOptions} from "@/routes/planner/-query"
import {
  EXPLORER_SKILLS_POSITIONS,
  EXPLORER_SKILL_CODES,
} from "@/routes/planner/-skill-codes"
import {useSuspenseQuery} from "@tanstack/react-query"
import {createFileRoute} from "@tanstack/react-router"

export const Route = createFileRoute("/planner/explorer")({
  loader: () =>
    queryClient.ensureQueryData(
      makePlannerQueryOptions(BaseClassType.Explorer, EXPLORER_SKILL_CODES),
    ),
  component: RouteComponent,
  preload: false,
})

function RouteComponent() {
  const {
    data: {
      all_player_skills: {skills},
    },
  } = useSuspenseQuery(
    makePlannerQueryOptions(BaseClassType.Explorer, EXPLORER_SKILL_CODES),
  )

  const groupedSkillData = groupSkillsData(skills)

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs
          items={[
            ...homeBreadcrumbItems,
            {label: "Planner Explorer", href: "/planner/explorer"},
          ]}
        />
        <PageTitle title="Explorer" />
      </PageHeader>
      <div className="flex flex-col items-center justify-around gap-10 lg:flex-row lg:items-start">
        <SkillPlannerCard
          skillData={groupedSkillData}
          positions={EXPLORER_SKILLS_POSITIONS}
          background="explorer"
          alwaysAllowedClasses={["is_explorer"]}
          classOptions={explorerClassOptions}
          levelOptions={landLevelOptions}
          getAvailableSkillPointsFromLevel={getAvailableSkillPointsLand}
        />
        <StatsPlannerCard baseClass={BaseClassType.Explorer} />
      </div>
    </>
  )
}
