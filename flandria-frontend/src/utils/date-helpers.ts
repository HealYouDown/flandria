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
