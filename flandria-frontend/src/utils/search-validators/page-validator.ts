import {fallback} from "@tanstack/router-zod-adapter"
import z from "zod"

export const pageValidator = fallback(z.number(), 1).default(1)
