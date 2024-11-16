import {Card, CardContent, CardHeader, CardTitle} from "@/components/ui/card"

interface DescriptionCardProps {
  title?: string
  description: string
}

export function DescriptionCard({
  title = "Description",
  description,
}: DescriptionCardProps) {
  const descriptionParts = description.split("\\n")

  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        {descriptionParts.map((part, i) => (
          <p key={i}>{part}</p>
        ))}
      </CardContent>
    </Card>
  )
}
