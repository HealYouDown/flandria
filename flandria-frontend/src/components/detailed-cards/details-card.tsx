import {
  Card,
  CardContentList,
  CardContentListItem,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

import React from "react"

export type Detail = {
  label: string
  description?: string
  value: string | JSX.Element
}

type DetailsCardProps = {
  details: Detail[]
  title?: string
}

type DetailCardItem = {
  label: string
  description?: string
  value: JSX.Element
}

export function DetailsCardItem({label, description, value}: DetailCardItem) {
  return (
    <CardContentListItem>
      <div className="flex items-center justify-between gap-x-4">
        <div className="flex flex-col">
          <span className="font-semibold tracking-tight">{label}</span>
          {description && (
            <p className="text-xs text-muted-foreground">{description}</p>
          )}
        </div>
        {value}
      </div>
    </CardContentListItem>
  )
}

export function DetailsCard({title = "Details", details}: DetailsCardProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContentList>
        {details.map((detail) => {
          let right = (
            <span className="whitespace-nowrap text-right">{detail.value}</span>
          )
          if (React.isValidElement(detail.value)) {
            right = detail.value
          }

          return (
            <DetailsCardItem
              label={detail.label}
              description={detail.description}
              value={right}
            />
          )
        })}
      </CardContentList>
    </Card>
  )
}
