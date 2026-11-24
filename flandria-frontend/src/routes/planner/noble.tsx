import {BaseClassType} from "@/lib/enums"
import {queryClient} from "@/lib/react-query-client"

import {plannerSearchValidator} from "@/components/planner/use-planner-build"

import {
  landLevelOptions,
  nobleClassOptions,
} from "@/routes/planner/-combobox-options"
import {
  PlannerConfig,
  PlannerPage,
  plannerQueryOptions,
} from "@/routes/planner/-planner-page"
import {NOBLE_SKILL_POSITIONS} from "@/routes/planner/-skill-codes"
import {createFileRoute} from "@tanstack/react-router"

const config: PlannerConfig<keyof typeof NOBLE_SKILL_POSITIONS> = {
  baseClass: BaseClassType.Noble,
  title: "Noble",
  href: "/planner/noble",
  positions: NOBLE_SKILL_POSITIONS,
  background: "noble",
  alwaysAllowedClasses: ["is_noble"],
  classOptions: nobleClassOptions,
  levelOptions: landLevelOptions,
}

export const Route = createFileRoute("/planner/noble")({
  loader: () => queryClient.ensureQueryData(plannerQueryOptions(config)),
  validateSearch: plannerSearchValidator,
  component: () => <PlannerPage config={config} />,
})
