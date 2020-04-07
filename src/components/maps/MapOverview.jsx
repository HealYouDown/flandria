import React from "react";
import { Row, Col } from "react-grid-system";
import Card, { CardHeader, CardListBody, ClickableCardListItem } from "../common/Card";


const MapOverview = () => {
  document.title = "Maps";

  const urls = [
    [
      {
        name: "Cardiff Island",
        urls: [
          ["Weedridge", "/AF2_000"],
          ["Cardiff Abandoned Mine", "/AD1_000"],
          ["Larksdowns", "/AF1_000"],
          ["Fox Den", "/AD2_000"],
          ["Secret Laboratory", "/AD3_000"],
          ["[Elite] Fox Den", "/AD4_000"],
          ["[Elite] Cardiff Abandoned Mine", "/AD5_000"],
          ["Realm of Ruins", "/DF1_000"]
        ]
      },
      {
        name: "Chester Island",
        urls: [
          ["Rainbow Highland", "/EF1_000"],
          ["Droes Under Valley", "/ED2_000"],
          ["Droes Cave of Abyss", "/ED1_000"],
        ]
      },
      {
        name: "Pirates of Black Dragon Base",
        urls: [
          ["Hidden Port", "/SD2F1_000"],
          ["Pirates of Black Dragon Base", "/SD2_000"]
        ]
      },
      {
        name: "Hoomanil Ocean",
        urls: [
          ["Hoomanil Ocean", "/AS1_000"],
        ]
      }
    ],
    [
      {
        name: "Magnel Island",
        urls: [
          ["Castle Field", "/BF1_000"],
          ["The 1st Floor of Tulach Dungeon", "/BD1_000"],
          ["The 1st Ground of Tulach Dungeon", "/BD2_000"],
          ["The 2nd Basement of Tulach Dungeon", "/BD3_000"],
          ["Lava Plateau", "/BF2_000"],
        ]
      },
      {
        name: "Party Islands",
        urls: [
          ["Ron", "/SR1_000"],
          ["Kendal", "/SR2_000"],
          ["Cony", "/SR3_000"],
          ["Clouds", "/AI1_000"],
          ["Aria", "/AI2_000"],
          ["Misty", "/BI1_000"],
          ["Gem", "/BI3_000"],
          ["Ease", "/CI3_000"],
          ["Eva", "/CI5_000"],
          ["Celestyn", "/EI1_000"],
          ["Selina", "/EI4_000"],
        ]
      }
    ],
    [
      {
        name: "Exeter Island",
        urls: [
          ["Gloshire", "/CF1_000"],
          ["The 1st Basement of Avery Big Mansion", "/CD1_000"],
          ["The 2nd Basement of Avery Big Mansion", "/CD2_000"],
          ["The 3rd Basement of Avery Big Mansion", "/CD3_000"],
          ["Room of Pain", "/CD4_000"],
          ["Laboratory of Death", "/CD5_000"],
          ["Laboratory of Blood", "/CD6_000"],
          ["[Elite] The 1st Basement of Avery Big Mansion", "/CED1_000"],
          ["[Elite] The 2nd Basement of Avery Big Mansion", "/CED2_000"],
          ["[Elite] The 3rd Basement of Avery Big Mansion", "/CED3_000"],
          ["[Elite] Room of Pain", "/CED4_000"],
          ["[Elite] Laboratory of Death", "/CED5_000"],
          ["[Elite] Laboratory of Blood", "/CED6_000"],
        ]
      },
      {
        name: "Sea of Bone",
        urls: [
          ["Peregrine Falcon Hiding Place", "/SD1F1_000"],
          ["Sea of Bone", "/SD1_000"]
        ]
      }
    ]
  ]

  return (
    <Row>
      {urls.map(columns => {
        return (
          <Col md={4}>
            {columns.map(colData => {
              return (
                <Card>
                  <CardHeader>
                    <span className="card-title">{colData.name}</span>
                  </CardHeader>
                  <CardListBody>
                    <ul>
                      {colData.urls.map(url => {
                        return (
                          <ClickableCardListItem link={"/map" + url[1]}>
                            <span className="hover-white">{url[0]}</span>
                          </ClickableCardListItem>
                        )
                      })}
                    </ul>
                  </CardListBody>
                </Card>
              )
            })}
          </Col>
        )
      })
      }
    </Row>
  )
}

export default MapOverview;