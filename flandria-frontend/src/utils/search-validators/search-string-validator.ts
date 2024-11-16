import {fallback} from "@tanstack/router-zod-adapter"
import z from "zod"

export const searchStringValidator = fallback(z.string(), "").default("")
