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
  mercenaryClassOptions,
} from "@/routes/planner/-combobox-options"
import {makePlannerQueryOptions} from "@/routes/planner/-query"
import {
  MERCENARY_SKILLS_POSITIONS,
  MERCENARY_SKILL_CODES,
} from "@/routes/planner/-skill-codes"
import {useSuspenseQuery} from "@tanstack/react-query"
import {createFileRoute} from "@tanstack/react-router"

export const Route = createFileRoute("/planner/mercenary")({
  loader: () =>
    queryClient.ensureQueryData(
      makePlannerQueryOptions(BaseClassType.Mercenary, MERCENARY_SKILL_CODES),
    ),
  component: RouteComponent,
})

function RouteComponent() {
  const {
    data: {
      all_player_skills: {skills},
      player_level_stats: levelData,
      player_stats: statsData,
    },
  } = useSuspenseQuery(
    makePlannerQueryOptions(BaseClassType.Mercenary, MERCENARY_SKILL_CODES),
  )

  const groupedSkillData = groupSkillsData(skills)

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs
          items={[
            ...homeBreadcrumbItems,
            {label: "Planner Mercenary", href: "/planner/mercenary"},
          ]}
        />
        <PageTitle title="Mercenary" />
      </PageHeader>
      <div className="flex flex-col items-center justify-around gap-10 lg:flex-row lg:items-start">
        <SkillPlannerCard
          skillData={groupedSkillData}
          positions={MERCENARY_SKILLS_POSITIONS}
          background="mercenary"
          alwaysAllowedClasses={["is_mercenary"]}
          classOptions={mercenaryClassOptions}
          levelOptions={landLevelOptions}
          getAvailableSkillPointsFromLevel={getAvailableSkillPointsLand}
        />
        <StatsPlannerCard
          baseClass={BaseClassType.Mercenary}
          levelData={levelData}
          statsData={statsData}
        />
      </div>
    </>
  )
}
