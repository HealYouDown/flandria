import React from 'react';
import { setWindowTitle } from '../../helpers';
import Card, { ClickableCardItem, CardHeader, CardHeaderTitle } from '../shared/Card';
import Grid, { Column } from '../shared/Grid';

const URLS = [
  [
    {
      name: 'Cardiff Island',
      urls: [
        ['Weedridge', '/map/AF2_000'],
        ['Cardiff Abandoned Mine', '/map/AD1_000'],
        ['Larksdowns', '/map/AF1_000'],
        ['Fox Den', '/map/AD2_000'],
        ['Secret Laboratory', '/map/AD3_000'],
        ['[Elite] Fox Den', '/map/AD4_000'],
        ['[Elite] Cardiff Abandoned Mine', '/map/AD5_000'],
      ],
    },
    {
      name: 'Chester Island',
      urls: [
        ['Rainbow Highland', '/map/EF1_000'],
        ['Droes Under Valley', '/map/ED2_000'],
        ['Droes Cave of Abyss', '/map/ED1_000'],
      ],
    },
    {
      name: 'Pirates of Black Dragon Base',
      urls: [
        ['Hidden Port', '/map/SD2F1_000'],
        ['Pirates of Black Dragon Base', '/map/SD2_000'],
      ],
    },
    {
      name: 'Hoomanil Ocean',
      urls: [
        ['Hoomanil Ocean', '/map/AS1_000'],
      ],
    },
  ],
  [
    {
      name: 'Magnel Island',
      urls: [
        ['Castle Field', '/map/BF1_000'],
        ['The 1st Floor of Tulach Dungeon', '/map/BD1_000'],
        ['The 1st Ground of Tulach Dungeon', '/map/BD2_000'],
        ['The 2nd Basement of Tulach Dungeon', '/map/BD3_000'],
        ['Lava Plateau', '/map/BF2_000'],
        ['Realm of Ruins', '/map/DF1_000'],
      ],
    },
    {
      name: 'Party Islands',
      urls: [
        ['Ron', '/map/SR1_000'],
        ['Kendal', '/map/SR2_000'],
        ['Cony', '/map/SR3_000'],
        ['Clouds', '/map/AI1_000'],
        ['Aria', '/map/AI2_000'],
        ['Misty', '/map/BI1_000'],
        ['Gem', '/map/BI3_000'],
        ['Ease', '/map/CI3_000'],
        ['Eva', '/map/CI5_000'],
        ['Celestyn', '/map/EI1_000'],
        ['Selina', '/map/EI4_000'],
      ],
    },
  ],
  [
    {
      name: 'Exeter Island',
      urls: [
        ['Gloshire', '/map/CF1_000'],
        ['The 1st Basement of Avery Big Mansion', '/map/CD1_000'],
        ['The 2nd Basement of Avery Big Mansion', '/map/CD2_000'],
        ['The 3rd Basement of Avery Big Mansion', '/map/CD3_000'],
        ['Room of Pain', '/map/CD4_000'],
        ['Laboratory of Death', '/map/CD5_000'],
        ['Laboratory of Blood', '/map/CD6_000'],
        ['[Elite] The 1st Basement of Avery Big Mansion', '/map/CED1_000'],
        ['[Elite] The 2nd Basement of Avery Big Mansion', '/map/CED2_000'],
        ['[Elite] The 3rd Basement of Avery Big Mansion', '/map/CED3_000'],
        ['[Elite] Room of Pain', '/map/CED4_000'],
        ['[Elite] Laboratory of Death', '/map/CED5_000'],
        ['[Elite] Laboratory of Blood', '/map/CED6_000'],
      ],
    },
    {
      name: 'Sea of Bone',
      urls: [
        ['Peregrine Falcon Hiding Place', '/map/SD1F1_000'],
        ['Sea of Bone', '/map/SD1_000'],
      ],
    },
  ],
];

const MapsOverview = () => {
  setWindowTitle('Maps Overview');

  return (
    <Grid gap="gap-6 gap-x-8">
      {URLS.map((column) => (
        <Column gap="gap-6" md={4}>
          {column.map((section) => (
            <Card
              header={(
                <CardHeader>
                  <CardHeaderTitle>{section.name}</CardHeaderTitle>
                </CardHeader>
              )}
            >
              <div className="divide-y divide-gray-200 dark:divide-dark-4">
                {section.urls.map((url) => (
                  <ClickableCardItem
                    to={url[1]}
                    key={url[1]}
                  >
                    {url[0]}
                  </ClickableCardItem>
                ))}
              </div>
            </Card>
          ))}
        </Column>
      ))}
    </Grid>
  );
};

export default MapsOverview;
