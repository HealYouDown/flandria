import {cn} from "@/lib/utils"

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

export type ComboboxOption<T> = {
  value: T
  label: string
}

interface ComboboxCommonProps<T> {
  options: ComboboxOption<T>[]
  id: string
  contentClassName?: string
  triggerClassName?: string
  placeholder?: string
  disabled?: boolean
}

interface ComboboxPropsNullable<T> extends ComboboxCommonProps<T> {
  nullable: true
  value: T | null
  onValueChange: (value: T | null) => void
}

interface ComboboxPropsNonNullable<T> extends ComboboxCommonProps<T> {
  nullable: false
  value: T
  onValueChange: (value: T) => void
}

type ComboboxProps<T> = ComboboxPropsNullable<T> | ComboboxPropsNonNullable<T>

export function Combobox<T>({
  options,
  value,
  id,
  onValueChange,
  triggerClassName,
  contentClassName,
  nullable,
  disabled = false,
  placeholder = "Select...",
}: ComboboxProps<T>) {
  const [open, setOpen] = React.useState(false)

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          id={id}
          variant="outline"
          role="combobox"
          aria-expanded={open}
          className={cn(triggerClassName, "justify-between")}
          disabled={disabled}
        >
          {value
            ? options.find((opt) => opt.value === value)?.label
            : placeholder}
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
                    const isSelfSelected =
                      optValue !== null && optValue == value

                    if (!nullable && isSelfSelected) return
                    const newValue = isSelfSelected ? null : (optValue as T)

                    setOpen(false)
                    onValueChange(newValue!)
                  }}
                >
                  <CheckIcon
                    className={cn(
                      "mr-2 h-4 w-4",
                      value === opt.value ? "opacity-100" : "opacity-0",
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
