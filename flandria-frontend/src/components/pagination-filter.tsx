import {cn} from "@/lib/utils"

import {Button} from "@/components/ui/button"
import {Label} from "@/components/ui/label"
import {Popover, PopoverContent, PopoverTrigger} from "@/components/ui/popover"

import {Settings2Icon} from "lucide-react"
import * as React from "react"

export type FilterMenuChildrenRenderProps = {
  Section: typeof SectionWrapper
  Label: typeof FilterLabel
}

type FilterMenuProps = {
  children: (props: FilterMenuChildrenRenderProps) => React.ReactNode
}

function SectionWrapper({
  children,
  className,
  ...props
}: React.ComponentProps<"div">) {
  return (
    <div {...props} className={cn(className, "grid grid-cols-3 items-center")}>
      {children}
    </div>
  )
}
const FilterLabel = Label

export function FilterMenu({children}: FilterMenuProps) {
  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button variant="outline" className="flex items-center gap-2">
          <span className="font-semibold">Filters</span>
          <Settings2Icon className="h-4 w-4" />
        </Button>
      </PopoverTrigger>
      <PopoverContent align="end" className="w-80">
        <div className="flex flex-col gap-2">
          {children({Section: SectionWrapper, Label: FilterLabel})}
        </div>
      </PopoverContent>
    </Popover>
  )
}

export function Filter({className, ...props}: React.ComponentProps<"div">) {
  return (
    <div className={cn(className, "flex justify-between gap-4")} {...props}>
      {props.children}
    </div>
  )
}
