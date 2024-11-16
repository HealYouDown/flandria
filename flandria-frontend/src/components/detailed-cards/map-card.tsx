import {
  MapCanvas,
  MapCanvasDetails,
  MonsterPosition,
  NPCPosition,
} from "@/components/map-canvas"
import {Card, CardContent, CardHeader, CardTitle} from "@/components/ui/card"
import {Tabs} from "@/components/ui/tabs"
import {TabsContent, TabsList, TabsTrigger} from "@/components/ui/tabs"

import * as React from "react"

export type MapDetails = {
  map: MapCanvasDetails
  positions: (MonsterPosition | NPCPosition)[]
}

interface MapCardProps {
  maps: MapDetails[]
}

export function MapCard({maps}: MapCardProps) {
  // Need to lift up the state from tabs, as it wouldn't re-render and select the new first tab when navigating from monster to monster
  const [selectedTab, setSelectedTab] = React.useState<string>()
  React.useEffect(() => {
    if (maps.length === 0) return
    setSelectedTab(maps[0].map.code)
  }, [maps])

  let body = (
    <CardContent>
      <p>No maps found.</p>
    </CardContent>
  )
  if (maps.length > 0) {
    body = (
      <CardContent className="p-2">
        <Tabs value={selectedTab} onValueChange={setSelectedTab}>
          <TabsList className="h-auto w-full flex-wrap justify-start">
            {maps.map((mapDetails) => (
              <TabsTrigger
                key={mapDetails.map.code}
                value={mapDetails.map.code}
              >
                {mapDetails.map.name}
              </TabsTrigger>
            ))}
          </TabsList>
          {maps.map((mapDetails) => (
            <TabsContent key={mapDetails.map.code} value={mapDetails.map.code}>
              <MapCanvas
                map={mapDetails.map}
                positions={mapDetails.positions}
                getColor={() => "#FF0000"}
                dotSizeDivisor={60}
              />
            </TabsContent>
          ))}
        </Tabs>
      </CardContent>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Maps</CardTitle>
      </CardHeader>
      {body}
    </Card>
  )
}
