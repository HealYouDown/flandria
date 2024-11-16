import {formatSeconds} from "@/utils/date-helpers"

import {graphql} from "@/gql"
import {SkillsCard_FragmentFragment} from "@/gql/graphql"

import {DetailsCardItem} from "@/components/detailed-cards/details-card"
import {GridItem} from "@/components/grid-item"
import {
  Card,
  CardContentList,
  CardContentListItem,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

graphql(`
  fragment SkillsCard_Fragment on SkillMixin {
    name
    description
    icon
    required_level_land
    required_level_sea
    cast_time
    cooldown
  }
`)

type SkillCardProps = {
  title?: string
  skill: SkillsCard_FragmentFragment
  extended?: boolean
}

export function SkillCard({title = "Skill", skill, extended}: SkillCardProps) {
  const extendedSection = (
    <>
      <DetailsCardItem
        label="Required Level"
        value={
          <span>
            {skill.required_level_land}/{skill.required_level_sea}
          </span>
        }
      />
      <DetailsCardItem
        label="Cast Time"
        value={<span>{formatSeconds(skill.cast_time)}</span>}
      />
      <DetailsCardItem
        label="Cooldown"
        value={<span>{formatSeconds(skill.cooldown)}</span>}
      />
    </>
  )

  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContentList>
        <CardContentListItem>
          <GridItem.NonLinkItem>
            <GridItem.Icon className="self-start" iconName={skill.icon} />
            <GridItem.Details>
              <GridItem.Name>{skill.name}</GridItem.Name>
              <GridItem.Subs subs={[skill.description]} />
            </GridItem.Details>
          </GridItem.NonLinkItem>
        </CardContentListItem>
        {extended && extendedSection}
      </CardContentList>
    </Card>
  )
}
