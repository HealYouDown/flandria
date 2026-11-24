import {BaseClassType} from "@/lib/enums"

import {ComboboxOption} from "@/components/combobox"
import {
  BreadcrumbItem,
  PageHeader,
  PageHeaderBreadcrumbs,
  PageTitle,
  homeBreadcrumbItems,
} from "@/components/page-header"
import {
  ClassFlagsType,
  SkillTree,
  groupSkillsData,
} from "@/components/planner/skill-helpers"
import {SkillPlannerCard} from "@/components/planner/skill-planner-card"
import {StatClass} from "@/components/planner/stat-formulas.generated"
import {StatsPlannerCard} from "@/components/planner/stats-planner-card"
import {usePlannerBuild} from "@/components/planner/use-planner-build"

import {makePlannerQueryOptions} from "@/routes/planner/-query"
import {useSuspenseQuery} from "@tanstack/react-query"
import * as React from "react"

export type PlannerConfig<TCode extends string> = {
  baseClass: BaseClassType
  title: string
  href: BreadcrumbItem["href"]
  positions: {[key in TCode]: {x: number; y: number}}
  background: "ship" | "explorer" | "noble" | "saint" | "mercenary"
  alwaysAllowedClasses: ClassFlagsType[]
  classOptions: ComboboxOption<ClassFlagsType>[] | null
  levelOptions: ComboboxOption<string>[]
}

export const plannerQueryOptions = <TCode extends string>(
  config: PlannerConfig<TCode>,
) => makePlannerQueryOptions(config.baseClass, Object.keys(config.positions))

export function PlannerPage<TCode extends string>({
  config,
}: {
  config: PlannerConfig<TCode>
}) {
  const {
    data: {
      all_player_skills: {skills},
    },
  } = useSuspenseQuery(plannerQueryOptions(config))

  const tree = React.useMemo(
    (): SkillTree<TCode> => ({
      skills: groupSkillsData<TCode>(skills),
      alwaysAllowedClasses: config.alwaysAllowedClasses,
      classOptions: config.classOptions?.map((o) => o.value) ?? null,
      maxLevel: config.levelOptions.length,
    }),
    [skills, config],
  )
  const {build, setBuild} = usePlannerBuild(tree)

  const {baseClass} = config

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs
          items={[
            ...homeBreadcrumbItems,
            {label: `Planner ${config.title}`, href: config.href},
          ]}
        />
        <PageTitle title={config.title} />
      </PageHeader>
      <div className="flex flex-col items-center justify-around gap-10 lg:flex-row lg:items-start">
        <SkillPlannerCard
          tree={tree}
          build={build}
          onChange={(skillBuild) => setBuild({...build, ...skillBuild})}
          positions={config.positions}
          background={config.background}
          classOptions={config.classOptions}
          levelOptions={config.levelOptions}
        />
        {baseClass !== BaseClassType.Ship && (
          <StatsPlannerCard
            baseClass={baseClass}
            // The base class flag doubles as the stat class without a second class
            statClass={
              (build.class ?? config.alwaysAllowedClasses[0]) as StatClass
            }
            levelLand={build.level}
            levelSea={build.levelSea}
            stats={build.stats}
            onChange={({levelLand, ...change}) =>
              setBuild({...build, ...change, level: levelLand ?? build.level})
            }
          />
        )}
      </div>
    </>
  )
}
