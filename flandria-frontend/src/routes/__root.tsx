import {Footer} from "@/components/footer"
import {NavMenu} from "@/components/nav-menu"
import {Toaster} from "@/components/ui/toaster"

import {ReactQueryDevtools} from "@tanstack/react-query-devtools"
import {
  Outlet,
  ScrollRestoration,
  createRootRoute,
} from "@tanstack/react-router"
import {TanStackRouterDevtools} from "@tanstack/router-devtools"

export const Route = createRootRoute({
  component: Root,
})

function Root() {
  return (
    <>
      <NavMenu />
      <main className="flex flex-grow flex-col px-4 py-8 md:px-10 lg:px-20 xl:px-40">
        <Outlet />
      </main>
      <Footer />
      <ScrollRestoration
        getKey={(loc) => {
          // Ignore scroll restoration for our planner. If we don't do this, we are
          // getting "restored" (read: the page jumps) everytime we click a skill, due to URL changes.
          if (loc.pathname.startsWith("/planner/")) {
            return loc.pathname
          }
          return loc.state.key!
        }}
      />
      <Toaster />

      {import.meta.env.DEV && (
        <>
          <TanStackRouterDevtools />
          <ReactQueryDevtools />
        </>
      )}
    </>
  )
}
