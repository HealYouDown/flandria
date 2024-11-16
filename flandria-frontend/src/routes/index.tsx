import {Link, createFileRoute} from "@tanstack/react-router"
import {ChevronRight} from "lucide-react"
import {useDocumentTitle} from "usehooks-ts"

export const Route = createFileRoute("/")({
  component: Index,
})

function Index() {
  useDocumentTitle("Home")

  return (
    <>
      <div
        className="absolute left-0 top-0 -z-50 h-screen w-screen bg-cover"
        style={{backgroundImage: "url(background.jpg)"}}
      />
      <div className="absolute left-0 top-0 -z-50 h-screen w-screen bg-black/30 dark:bg-black/60" />

      <div className="flex text-white dark:text-foreground md:mt-10 xl:mt-20">
        <div className="flex max-w-xl flex-col space-y-1">
          <h2 className="text-6xl font-bold tracking-tight xl:text-7xl">
            Welcome to Flandria
          </h2>
          <small className="text-2xl text-white/70 dark:text-muted-foreground">
            Your Florensia Database
          </small>
          <p className="text-xl">
            Flandria is an open-source database website for the MMORPG
            Florensia. It provides a clean interface for you to browse through
            all monsters, items and quests that exist in the world of Florensia.
            Also included are a character builder which allows you to design
            your own character skilltree.
          </p>
          <div className="py-2">
            <Link
              to="/database"
              className="flex max-w-min items-center justify-center space-x-2 rounded-md bg-black/50 px-6 py-2 text-center text-xl backdrop-blur transition-colors hover:bg-black/70 dark:text-foreground"
            >
              <span className="font-bold uppercase tracking-wider">
                Explore
              </span>
              <ChevronRight />
            </Link>
          </div>
        </div>
      </div>
    </>
  )
}
