import humanizeDuration from "humanize-duration"

const defaultHumanizer = humanizeDuration.humanizer({
  language: "en",
  units: ["d", "h", "m", "s", "ms"],
})

const shortHumanizer = humanizeDuration.humanizer({
  language: "shortEn",
  languages: {
    shortEn: {
      y: () => "y",
      mo: () => "mo",
      w: () => "w",
      d: () => "d",
      h: () => "h",
      m: () => "m",
      s: () => "s",
      ms: () => "ms",
    },
  },
})

export function isAprilFools(): boolean {
  const today = new Date()
  return today.getDate() === 1 && today.getMonth() === 3
}

export function formatMinutes(
  durationInMinutes: number,
  short: boolean = false,
): string {
  const ms = (durationInMinutes - 1) * 60 * 1000
  return short ? shortHumanizer(ms) : defaultHumanizer(ms)
}

export function formatSeconds(
  durationInSeconds: number,
  short: boolean = false,
): string {
  const ms = durationInSeconds * 1000
  return short ? shortHumanizer(ms) : defaultHumanizer(ms)
}

// Same as the client: the casting bar of land player skills runs 300ms longer
// than the table value, anything below 5ms is instant.
export function formatCastTime(
  castTimeInSeconds: number,
  isLandPlayerSkill: boolean,
): string {
  if (castTimeInSeconds < 0.005) return "Instant"
  const padded = castTimeInSeconds + (isLandPlayerSkill ? 0.3 : 0)
  return `${padded.toFixed(2)}s`
}
