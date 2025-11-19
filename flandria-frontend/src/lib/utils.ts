import {type ClassValue, clsx} from "clsx"
import {twMerge} from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatPercent(value: number, decimals: number = 2) {
  const percent = value * 100
  const rounded = Number(percent.toFixed(decimals))
  return rounded.toString().replace(/\.?0+$/, "") + "%"
}
