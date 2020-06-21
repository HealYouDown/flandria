import React from "react";
import { Row, Col } from "react-grid-system";
import Card, { CardHeader, CardListBody, ClickableCardListItem } from "../common/Card";


const TableOverview = () => {
  document.title = "Items";

  const urls = [
    [
      // Column 1
      {
        name: "Weapons",
        urls: [
          ["Cariads", "/cariad"],
          ["Rapiers", "/rapier"],
          ["Daggers", "/dagger"],
          ["One-handed Swords", "/one_handed_sword"],
          ["Two-handed Swords", "/two_handed_sword"],
          ["Shields", "/shield"],
          ["Rifles", "/rifle"],
          ["Duals", "/duals"],
        ]
      },
      {
        name: "Armor",
        urls: [
          ["Coats", "/coat"],
          ["Pants", "/pants"],
          ["Gauntlets", "/gauntlet"],
          ["Shoes", "/shoes"],
        ]
      },
      {
        name: "Quests",
        urls: [
          ["Quest Scrolls", "/quest_scroll"],
          ["Quest Items", "/quest_item"],
        ]
      }
    ],
    [
      // Column 2
      {
        name: "Extra Equipment",
        urls: [
          ["Hats", "/hat"],
          ["Dresses", "/dress"],
          ["Accessories", "/accessory"],
        ]
      },
      {
        name: "Essence",
        urls: [
          ["Essences", "/essence"],
          ["Essence Help Items", "/essence_help_item"],
          ["Essence Recipes", "/production?filter=prod_class:Essence"],
        ]
      },
      {
        name: "Crafting",
        urls: [
          ["Recipes", "/recipe"],
          ["Materials", "/material"],
          ["Second Job", "/production"],
        ]
      },
      {
        name: "Ship",
        urls: [
          ["Bodies", "/ship_body"],
          ["Fronts", "/ship_front"],
          ["Head Masts", "/ship_head_mast"],
          ["Main Masts", "/ship_main_mast"],
          ["Figures", "/ship_figure"],
          ["Magic Stones", "/ship_magic_stone"],
          ["Anchors", "/ship_anchor"],
          ["Shell", "/shell"],
          ["Flags", "/ship_flag"],
          ["Normal Weapon", "/ship_normal_weapon"],
          ["Special Weapon", "/ship_special_weapon"],
        ]
      }
    ],
    [
      // Column 3
      {
        name: "Pets",
        urls: [
          ["Combine Help Item", "/pet_combine_help"],
          ["Combine Stone Item", "/pet_combine_stone"],
          ["Pet Skills", "/pet_skill_stone"],
          ["Pets", "/pet"],
          ["Riding Pets", "/riding_pet"],
        ]
      },
      {
        name: "Enhancing",
        urls: [
          ["Seal Break Item", "/seal_break_help"],
          ["Upgrade Help Item", "/upgrade_help"],
          ["Upgrade Crystals", "/upgrade_crystal"],
          ["Upgrade Stone", "/upgrade_stone"],
        ]
      },
      {
        name: "Fishing",
        urls: [
          ["Fishing Rods", "/fishing_rod"],
          ["Fishing Items", "/fishing_material"],
          ["Fishing Baits", "/fishing_bait"],
        ]
      },
      {
        name: "Others",
        urls: [
          ["Random Boxes", "/random_box"],
          ["Consumables", "/consumable"],
          ["Bullets", "/bullet"],
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
                          <ClickableCardListItem link={"/database" + url[1]}>
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

export default TableOverview;