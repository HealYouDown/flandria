import {Link} from "@tanstack/react-router"

export function NotFoundComponent() {
  return (
    <div>
      <p>The requested page wasn't found.</p>
      <Link to="/">Back to home</Link>
    </div>
  )
}
