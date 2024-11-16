import {cn} from "@/lib/utils"

import {ComboboxOption} from "@/components/combobox"
import {Button} from "@/components/ui/button"
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command"
import {Popover, PopoverContent, PopoverTrigger} from "@/components/ui/popover"

import {CheckIcon, ChevronsUpDownIcon} from "lucide-react"
import * as React from "react"

interface MultiComboboxProps<T> {
  options: ComboboxOption<T>[]
  id: string
  contentClassName?: string
  triggerClassName?: string

  value: T[]
  onValueChange: (values: T[]) => void
}

export function MultiCombobox<T>({
  options,
  value,
  id,
  onValueChange,
  triggerClassName,
  contentClassName,
}: MultiComboboxProps<T>) {
  const [open, setOpen] = React.useState(false)
  const selectedOptions = options.filter((opt) => value.includes(opt.value))

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          id={id}
          variant="outline"
          role="combobox"
          aria-expanded={open}
          className={cn(triggerClassName, "justify-between")}
        >
          {selectedOptions.length > 0
            ? `${selectedOptions.length} selected`
            : // ? selectedOptions.map((opt) => opt.label).join(", ")
              "Select..."}
          <ChevronsUpDownIcon className="h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent align="end" className={cn(contentClassName, "p-0.5")}>
        <Command
          filter={(value, search) => {
            const option = options.find((opt) => opt.value === value)
            if (!option) return 0
            if (option.label.toLowerCase().includes(search.toLowerCase()))
              return 1
            return 0
          }}
        >
          <CommandInput placeholder="Search..." />
          <CommandList>
            <CommandEmpty>No result found.</CommandEmpty>
            <CommandGroup>
              {options.map((opt) => (
                <CommandItem
                  key={opt.value as React.Key}
                  value={opt.value === null ? undefined : (opt.value as string)}
                  onSelect={(optValue) => {
                    const isSelfSelected = value.includes(optValue as T)
                    const newValue = isSelfSelected
                      ? value.filter((v) => v != optValue)
                      : [...value, optValue as T]
                    onValueChange(newValue!)
                  }}
                >
                  <CheckIcon
                    className={cn(
                      "mr-2 h-4 w-4",
                      value.includes(opt.value) ? "opacity-100" : "opacity-0",
                    )}
                  />
                  {opt.label}
                </CommandItem>
              ))}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  )
}
