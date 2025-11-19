import {type ClassValue, clsx} from "clsx"
import {twMerge} from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatPercent(value: number) {
  return value.toLocaleString("en-US", {
    style: "percent",
    maximumFractionDigits: 6,
  })
}
