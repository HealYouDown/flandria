import {
  ClassFlagsType,
  SkillBuild,
  SkillTree,
  normalizeSkillBuild,
} from "@/components/planner/skill-helpers"
import {
  InvestedStats,
  MAX_INVEST_POINTS,
  NO_INVESTED_STATS,
} from "@/components/planner/stat-helpers"

import {useNavigate, useSearch} from "@tanstack/react-router"
import {fallback, zodSearchValidator} from "@tanstack/router-zod-adapter"
import * as React from "react"
import {z} from "zod"

// The build is stored in the url, so that it can be shared:
// p: skill tree (level, class, skills), s: stats (sea level, invested points).
// Both are base64 encoded JSON, kept for compatibility with existing links.
export const plannerSearchValidator = zodSearchValidator(
  z.object({
    p: fallback(z.string().optional(), undefined),
    s: fallback(z.string().optional(), undefined),
  }),
)

const statPoint = fallback(z.number().int().min(0).max(MAX_INVEST_POINTS), 0)

const skillsParamSchema = z.object({
  level: z.number(),
  class: fallback(z.string().nullable(), null),
  skills: fallback(z.record(z.number()), {}),
})

const statsParamSchema = z.object({
  levelSea: fallback(z.number().int().min(1), 1),
  // Old links stored the land level in the stats as well
  levelLand: z.number().int().optional(),
  strength: statPoint,
  dexterity: statPoint,
  constitution: statPoint,
  intelligence: statPoint,
  wisdom: statPoint,
  will: statPoint,
})

function decode<T>(value: string | undefined, schema: z.ZodType<T>): T | null {
  if (!value) return null
  try {
    return schema.parse(JSON.parse(atob(value)))
  } catch {
    return null
  }
}

const encode = (value: unknown) => btoa(JSON.stringify(value))

export type PlannerBuild<TCode extends string> = SkillBuild<TCode> & {
  levelSea: number
  stats: InvestedStats
}

export function usePlannerBuild<TCode extends string>(tree: SkillTree<TCode>) {
  const search = useSearch({strict: false}) as {p?: string; s?: string}
  const navigate = useNavigate()

  const build = React.useMemo((): PlannerBuild<TCode> => {
    const skillsParam = decode(search.p, skillsParamSchema)
    const statsParam = decode(search.s, statsParamSchema)
    const {levelSea, levelLand, ...stats} = statsParam ?? {
      levelSea: 1,
      levelLand: undefined,
      ...NO_INVESTED_STATS,
    }

    const skillBuild = normalizeSkillBuild(
      {
        level: skillsParam?.level ?? levelLand ?? 1,
        class: (skillsParam?.class as ClassFlagsType | null) ?? null,
        skills: (skillsParam?.skills ?? {}) as SkillBuild<TCode>["skills"],
      },
      tree,
    )
    return {...skillBuild, levelSea, stats}
  }, [search.p, search.s, tree])

  const setBuild = React.useCallback(
    (next: PlannerBuild<TCode>) => {
      const {levelSea, stats, ...skillBuild} = next
      const normalized = normalizeSkillBuild(skillBuild, tree)

      const hasSkills = Object.values<number>(normalized.skills).some(
        (lv) => lv > 0,
      )
      const isInitialSkills =
        normalized.level === 1 && normalized.class === null && !hasSkills
      const isInitialStats =
        levelSea === 1 && Object.values(stats).every((v) => v === 0)

      navigate({
        to: ".",
        search: (prev: Record<string, unknown>) => ({
          ...prev,
          p: isInitialSkills ? undefined : encode(normalized),
          s: isInitialStats ? undefined : encode({levelSea, ...stats}),
        }),
        replace: true,
        resetScroll: false,
      })
    },
    [navigate, tree],
  )

  return {build, setBuild}
}
