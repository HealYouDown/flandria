import {BaseClassType} from "@/lib/enums"
import {queryClient} from "@/lib/react-query-client"

import {plannerSearchValidator} from "@/components/planner/use-planner-build"

import {
  explorerClassOptions,
  landLevelOptions,
} from "@/routes/planner/-combobox-options"
import {
  PlannerConfig,
  PlannerPage,
  plannerQueryOptions,
} from "@/routes/planner/-planner-page"
import {EXPLORER_SKILLS_POSITIONS} from "@/routes/planner/-skill-codes"
import {createFileRoute} from "@tanstack/react-router"

const config: PlannerConfig<keyof typeof EXPLORER_SKILLS_POSITIONS> = {
  baseClass: BaseClassType.Explorer,
  title: "Explorer",
  href: "/planner/explorer",
  positions: EXPLORER_SKILLS_POSITIONS,
  background: "explorer",
  alwaysAllowedClasses: ["is_explorer"],
  classOptions: explorerClassOptions,
  levelOptions: landLevelOptions,
}

export const Route = createFileRoute("/planner/explorer")({
  loader: () => queryClient.ensureQueryData(plannerQueryOptions(config)),
  preload: false,
  validateSearch: plannerSearchValidator,
  component: () => <PlannerPage config={config} />,
})
