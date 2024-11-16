import {UseNavigateResult} from "@tanstack/react-router"
import {SearchIcon} from "lucide-react"
import {useDebounceCallback} from "usehooks-ts"

interface SearchBarProps {
  value: string
  // technically, we'd need to list all routes.. but whatever
  navigate: UseNavigateResult<"/">
}

export function FilterSearchBar({value, navigate}: SearchBarProps) {
  const debounced = useDebounceCallback((val) => {
    navigate({search: (prev) => ({...prev, page: 1, s: val})})
  }, 500)

  return (
    <div className="flex h-10 w-full items-center gap-2 rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground has-[:focus-visible]:outline-none has-[:focus-visible]:ring-2 has-[:focus-visible]:ring-ring has-[:focus-visible]:ring-offset-2">
      <SearchIcon className="h-[1.2rem] w-[1rem]" />
      <input
        defaultValue={value}
        className="w-full border-none bg-transparent shadow-none outline-none"
        type="search"
        onChange={(event) => debounced(event.target.value)}
      />
    </div>
  )
}
