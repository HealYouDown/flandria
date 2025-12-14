import {ColsWrapper} from "@/components/cols-wrapper"
import {
  BreadcrumbItem,
  PageHeader,
  PageHeaderBreadcrumbs,
  PageTitle,
  databaseBreadcrumbItems,
} from "@/components/page-header"
import {
  Card,
  CardContentList,
  CardHeader,
  CardTitle,
  CardContentLinkListItem as ListItem,
} from "@/components/ui/card"

import {createFileRoute} from "@tanstack/react-router"

export const Route = createFileRoute("/database/map")({
  component: DatabaseIndex,
})

interface MapListItem extends React.ComponentProps<typeof ListItem> {
  code: string
}
const MapListItem = ({code, children}: MapListItem) => (
  <ListItem from={Route.fullPath} to="$code" params={{code: code}}>
    {children}
  </ListItem>
)

const Cardiff = (
  <Card>
    <CardHeader>
      <CardTitle>Cardiff Island</CardTitle>
    </CardHeader>
    <CardContentList>
      <MapListItem code="AC1_000">Roxbury</MapListItem>
      <MapListItem code="AF2_000">Weedridge</MapListItem>
      <MapListItem code="AD1_000">Cardiff Abandoned Mine</MapListItem>
      <MapListItem code="AF1_000">Larksdowns</MapListItem>
      <MapListItem code="AD2_000">Fox Den</MapListItem>
      <MapListItem code="AD3_000">Secret Laboratory</MapListItem>
      <MapListItem code="AD4_000">[Elite] Fox Den</MapListItem>
      <MapListItem code="AD5_000">[Elite] Cardiff Abandoned Mine</MapListItem>
      <MapListItem code="DF1_000">Realm of Ruins</MapListItem>
    </CardContentList>
  </Card>
)

const Magnel = (
  <Card>
    <CardHeader>
      <CardTitle>Magnel Island</CardTitle>
    </CardHeader>
    <CardContentList>
      <MapListItem code="BC1_000">Castle Hall</MapListItem>
      <MapListItem code="BF1_000">Castle Field</MapListItem>
      <MapListItem code="BD1_000">The 1st Floor of Tulach Dungeon</MapListItem>
      <MapListItem code="BD2_000">The 1st Ground of Tulach Dungeon</MapListItem>
      <MapListItem code="BD3_000">
        The 2nd Basement of Tulach Dungeon
      </MapListItem>
      <MapListItem code="BF2_000">Lava Plateau</MapListItem>
    </CardContentList>
  </Card>
)

const Exeter = (
  <Card>
    <CardHeader>
      <CardTitle>Exeter Island</CardTitle>
    </CardHeader>
    <CardContentList>
      <MapListItem code="CC1_000">Glostern</MapListItem>
      <MapListItem code="CF1_000">Gloshire</MapListItem>
      <MapListItem code="CD1_000">
        The 1st Basement of Avery Big Mansion
      </MapListItem>
      <MapListItem code="CD2_000">
        The 2nd Basement of Avery Big Mansion
      </MapListItem>
      <MapListItem code="CD3_000">
        The 3rd Basement of Avery Big Mansion
      </MapListItem>
      <MapListItem code="CD4_000">Room of Pain</MapListItem>
      <MapListItem code="CD5_000">Laboratory of Death</MapListItem>
      <MapListItem code="CD6_000">Laboratory of Blood</MapListItem>
      <MapListItem code="CED1_000">
        [Elite] The 1st Basement of Avery Big Mansion
      </MapListItem>
      <MapListItem code="CED2_000">
        [Elite] The 2nd Basement of Avery Big Mansion
      </MapListItem>
      <MapListItem code="CED3_000">
        [Elite] The 3rd Basement of Avery Big Mansion
      </MapListItem>
      <MapListItem code="CED4_000">[Elite] Room of Pain</MapListItem>
      <MapListItem code="CED5_000">[Elite] Laboratory of Death</MapListItem>
      <MapListItem code="CED6_000">[Elite] Laboratory of Blood</MapListItem>
    </CardContentList>
  </Card>
)

const Chester = (
  <Card>
    <CardHeader>
      <CardTitle>Chester Island</CardTitle>
    </CardHeader>
    <CardContentList>
      <MapListItem code="EC1_000">Cherrytown</MapListItem>
      <MapListItem code="EF1_000">Rainbow Highland</MapListItem>
      <MapListItem code="ED2_000">Droes Under Valley</MapListItem>
      <MapListItem code="ED1_000">Droes Cave of Abyss</MapListItem>
      <MapListItem code="ED3_000">Valley of Decay</MapListItem>
      <MapListItem code="ED4_000">Devouring Abyss</MapListItem>
    </CardContentList>
  </Card>
)

const PartyIslands = (
  <Card>
    <CardHeader>
      <CardTitle>Party Islands</CardTitle>
    </CardHeader>
    <CardContentList>
      <MapListItem code="SR1_000">Ron</MapListItem>
      <MapListItem code="SR2_000">Kendal</MapListItem>
      <MapListItem code="SR3_000">Cony</MapListItem>
      <MapListItem code="AI1_000">Clouds</MapListItem>
      <MapListItem code="AI2_000">Aria</MapListItem>
      <MapListItem code="BI1_000">Misty</MapListItem>
      <MapListItem code="BI3_000">Gem</MapListItem>
      <MapListItem code="CI3_000">Ease</MapListItem>
      <MapListItem code="CI5_000">Eva</MapListItem>
      <MapListItem code="EI1_000">Celestyn</MapListItem>
      <MapListItem code="EI4_000">Selina</MapListItem>
    </CardContentList>
  </Card>
)

const BlackDragonBase = (
  <Card>
    <CardHeader>
      <CardTitle>Pirates of Black Dragon Base</CardTitle>
    </CardHeader>
    <CardContentList>
      <MapListItem code="SD2F1_000">Hidden Port</MapListItem>
      <MapListItem code="SD2_000">Pirates of Black Dragon Base</MapListItem>
    </CardContentList>
  </Card>
)

const SeaOfBones = (
  <Card>
    <CardHeader>
      <CardTitle>Sea of Bones</CardTitle>
    </CardHeader>
    <CardContentList>
      <MapListItem code="SD1F1_000">Peregrine Falcon Hiding Place</MapListItem>
      <MapListItem code="SD1_000">Sea of Bone</MapListItem>
    </CardContentList>
  </Card>
)

const Ocean = (
  <Card>
    <CardHeader>
      <CardTitle>Hoomanil Ocean</CardTitle>
    </CardHeader>
    <CardContentList>
      <MapListItem code="AS1_000">Hoomanil Ocean</MapListItem>
    </CardContentList>
  </Card>
)

export const mapBreadcrumbItems: BreadcrumbItem[] = [
  ...databaseBreadcrumbItems,
  {label: "Maps", href: "/database/map"},
]

function DatabaseIndex() {
  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs items={mapBreadcrumbItems} />
        <PageTitle title="Maps" />
      </PageHeader>
      <ColsWrapper>
        <div>
          {Cardiff}
          {Chester}
          {BlackDragonBase}
          {Ocean}
        </div>
        <div>
          {Magnel}
          {PartyIslands}
        </div>
        <div>
          {Exeter}
          {SeaOfBones}
        </div>
      </ColsWrapper>
    </>
  )
}
