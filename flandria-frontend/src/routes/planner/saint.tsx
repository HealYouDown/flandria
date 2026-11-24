import {BaseClassType} from "@/lib/enums"
import {queryClient} from "@/lib/react-query-client"

import {plannerSearchValidator} from "@/components/planner/use-planner-build"

import {
  landLevelOptions,
  saintClassOptions,
} from "@/routes/planner/-combobox-options"
import {
  PlannerConfig,
  PlannerPage,
  plannerQueryOptions,
} from "@/routes/planner/-planner-page"
import {SAINT_SKILLS_POSITIONS} from "@/routes/planner/-skill-codes"
import {createFileRoute} from "@tanstack/react-router"

const config: PlannerConfig<keyof typeof SAINT_SKILLS_POSITIONS> = {
  baseClass: BaseClassType.Saint,
  title: "Saint",
  href: "/planner/saint",
  positions: SAINT_SKILLS_POSITIONS,
  background: "saint",
  alwaysAllowedClasses: ["is_saint"],
  classOptions: saintClassOptions,
  levelOptions: landLevelOptions,
}

export const Route = createFileRoute("/planner/saint")({
  loader: () => queryClient.ensureQueryData(plannerQueryOptions(config)),
  validateSearch: plannerSearchValidator,
  component: () => <PlannerPage config={config} />,
})
