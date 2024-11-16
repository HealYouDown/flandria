import {PendingComponent} from "@/components/pending-component"

import {createFileRoute} from "@tanstack/react-router"

export const Route = createFileRoute("/experimental/dodo-loading")({
  component: () => (
    <div className="flex grow">
      <PendingComponent />
    </div>
  ),
})
