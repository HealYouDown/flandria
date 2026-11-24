import {BaseClassType} from "@/lib/enums"
import {queryClient} from "@/lib/react-query-client"

import {plannerSearchValidator} from "@/components/planner/use-planner-build"

import {
  landLevelOptions,
  mercenaryClassOptions,
} from "@/routes/planner/-combobox-options"
import {
  PlannerConfig,
  PlannerPage,
  plannerQueryOptions,
} from "@/routes/planner/-planner-page"
import {MERCENARY_SKILLS_POSITIONS} from "@/routes/planner/-skill-codes"
import {createFileRoute} from "@tanstack/react-router"

const config: PlannerConfig<keyof typeof MERCENARY_SKILLS_POSITIONS> = {
  baseClass: BaseClassType.Mercenary,
  title: "Mercenary",
  href: "/planner/mercenary",
  positions: MERCENARY_SKILLS_POSITIONS,
  background: "mercenary",
  alwaysAllowedClasses: ["is_mercenary"],
  classOptions: mercenaryClassOptions,
  levelOptions: landLevelOptions,
}

export const Route = createFileRoute("/planner/mercenary")({
  loader: () => queryClient.ensureQueryData(plannerQueryOptions(config)),
  validateSearch: plannerSearchValidator,
  component: () => <PlannerPage config={config} />,
})
