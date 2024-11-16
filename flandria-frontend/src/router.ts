import {NotFoundComponent} from "@/components/not-found-component"
import {PendingComponent} from "@/components/pending-component"

import {routeTree} from "./routeTree.gen"

import {createRouter} from "@tanstack/react-router"

export const router = createRouter({
  routeTree,
  // threshold when to show the pending animatiojn
  defaultPendingMs: 1000,
  // how long to pending animation should be shown at minimum to avoid flashes
  defaultPendingMinMs: 700,
  defaultNotFoundComponent: NotFoundComponent,
  defaultPendingComponent: PendingComponent,
})

declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router
  }
}
