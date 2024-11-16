import {ThemeProvider} from "@/lib/theme-provider"

import {TooltipProvider} from "@/components/ui/tooltip"

import "./index.css"
import {queryClient} from "./lib/react-query-client"

import {router} from "@/router"
import {QueryClientProvider} from "@tanstack/react-query"
import {RouterProvider} from "@tanstack/react-router"
import * as React from "react"
import ReactDOM from "react-dom/client"

const rootElement = document.getElementById("root")!
if (!rootElement.innerHTML) {
  const root = ReactDOM.createRoot(rootElement)
  root.render(
    <React.StrictMode>
      <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
        <QueryClientProvider client={queryClient}>
          <TooltipProvider>
            <RouterProvider router={router} />
          </TooltipProvider>
        </QueryClientProvider>
      </ThemeProvider>
    </React.StrictMode>,
  )
}
