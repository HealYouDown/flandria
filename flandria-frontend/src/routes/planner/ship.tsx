import {BaseClassType} from "@/lib/enums"
import {queryClient} from "@/lib/react-query-client"

import {plannerSearchValidator} from "@/components/planner/use-planner-build"

import {seaLevelOptions} from "@/routes/planner/-combobox-options"
import {
  PlannerConfig,
  PlannerPage,
  plannerQueryOptions,
} from "@/routes/planner/-planner-page"
import {SHIP_SKILL_POSITIONS} from "@/routes/planner/-skill-codes"
import {createFileRoute} from "@tanstack/react-router"

const config: PlannerConfig<keyof typeof SHIP_SKILL_POSITIONS> = {
  baseClass: BaseClassType.Ship,
  title: "Ship",
  href: "/planner/ship",
  positions: SHIP_SKILL_POSITIONS,
  background: "ship",
  alwaysAllowedClasses: [
    "is_torpedo",
    "is_armored",
    "is_assault",
    "is_big_gun",
    "is_maintenance",
  ],
  classOptions: null,
  levelOptions: seaLevelOptions,
}

export const Route = createFileRoute("/planner/ship")({
  loader: () => queryClient.ensureQueryData(plannerQueryOptions(config)),
  validateSearch: plannerSearchValidator,
  component: () => <PlannerPage config={config} />,
})
