import React from "react";
import { Row, Col } from 'react-grid-system';

import CardList, { ClickableListItem } from "../../shared/CardList";

export default class Overview extends React.Component {
  componentDidMount() {
    document.title = "Items";
  }

  render() {
    return (
      <Row>
        <Col md={4}>
          <CardList header={true} list={true}>
            <span className="card-title">Weapons</span>
            <ClickableListItem link="/database/cariad">Cariads</ClickableListItem>
            <ClickableListItem link="/database/rapier">Rapiers</ClickableListItem>
            <ClickableListItem link="/database/dagger">Daggers</ClickableListItem>
            <ClickableListItem link="/database/one_handed_sword">One-handed Swords</ClickableListItem>
            <ClickableListItem link="/database/two_handed_sword">Two-handed Swords</ClickableListItem>
            <ClickableListItem link="/database/shield">Shields</ClickableListItem>
            <ClickableListItem link="/database/rifle">Rifles</ClickableListItem>
            <ClickableListItem link="/database/duals">Duals</ClickableListItem>
          </CardList>

          <CardList header={true} list={true}>
            <span className="card-title">Armor</span>
            <ClickableListItem link="/database/coat">Coats</ClickableListItem>
            <ClickableListItem link="/database/pants">Pants</ClickableListItem>
            <ClickableListItem link="/database/gauntlet">Gauntlets</ClickableListItem>
            <ClickableListItem link="/database/shoes">Shoes</ClickableListItem>
          </CardList>

          <CardList header={true} list={true}>
            <span className="card-title">Quests</span>
            <ClickableListItem link="/database/quest_scroll">Quest Scrolls</ClickableListItem>
            <ClickableListItem link="/database/quest_item">Quest Items</ClickableListItem>
          </CardList>
        </Col>

        <Col md={4}>
          <CardList header={true} list={true}>
            <span className="card-title">Extra Equipment</span>
            <ClickableListItem link="/database/hat">Hats</ClickableListItem>
            <ClickableListItem link="/database/dress">Dresses</ClickableListItem>
            <ClickableListItem link="/database/accessory">Accessories</ClickableListItem>
          </CardList>

          <CardList header={true} list={true}>
            <span className="card-title">Crafting</span>
            <ClickableListItem link="/database/recipe">Recipes</ClickableListItem>
            <ClickableListItem link="/database/material">Materials</ClickableListItem>
            <ClickableListItem link="/database/product_book">Second Job</ClickableListItem>
          </CardList>

          <CardList header={true} list={true}>
            <span className="card-title">Ship</span>
            <ClickableListItem link="/database/ship_body">Bodies</ClickableListItem>
            <ClickableListItem link="/database/ship_front">Ship Front</ClickableListItem>
            <ClickableListItem link="/database/ship_head_mast">Head Mast</ClickableListItem>
            <ClickableListItem link="/database/ship_main_mast">Main Mast</ClickableListItem>
            <ClickableListItem link="/database/ship_figure">Figures</ClickableListItem>
            <ClickableListItem link="/database/ship_magic_stone">Magic Stone</ClickableListItem>
            <ClickableListItem link="/database/ship_anchor">Anchors</ClickableListItem>
            <ClickableListItem link="/database/shell">Shells</ClickableListItem>
            <ClickableListItem link="/database/ship_flag">Flag</ClickableListItem>
            <ClickableListItem link="/database/ship_normal_weapon">Normal Weapon</ClickableListItem>
            <ClickableListItem link="/database/ship_special_weapon">Special Weapon</ClickableListItem>
          </CardList>
        </Col>

        <Col md={4}>
          <CardList header={true} list={true}>
            <span className="card-title">Pets</span>
            <ClickableListItem link="/database/pet_combine_help">Combine Help Item</ClickableListItem>
            <ClickableListItem link="/database/pet_combine_stone">Combine Stone Item</ClickableListItem>
            <ClickableListItem link="/database/pet_skill_stone">Pet Skills</ClickableListItem>
            <ClickableListItem link="/database/pet">Pets</ClickableListItem>
            <ClickableListItem link="/database/riding_pet">Riding Pets</ClickableListItem>
          </CardList>

          <CardList header={true} list={true}>
            <span className="card-title">Enhancing</span>
            <ClickableListItem link="/database/seal_break_help">Seal Break Item</ClickableListItem>
            <ClickableListItem link="/database/upgrade_help">Upgrade Help Item</ClickableListItem>
            <ClickableListItem link="/database/upgrade_crystal">Upgrade Crystals</ClickableListItem>
            <ClickableListItem link="/database/upgrade_stone">Upgrade Stones</ClickableListItem>
          </CardList>

          <CardList header={true} list={true}>
            <span className="card-title">Fishing</span>
            <ClickableListItem link="/database/fishing_rod">Fishing Rods</ClickableListItem>
            <ClickableListItem link="/database/fishing_material">Fishing Items</ClickableListItem>
            <ClickableListItem link="/database/fishing_bait">Fishing Baits</ClickableListItem>
          </CardList>

          <CardList header={true} list={true}>
            <span className="card-title">Fishing</span>
            <ClickableListItem link="/database/random_box">Random Boxes</ClickableListItem>
            <ClickableListItem link="/database/consumable">Consumables</ClickableListItem>
            <ClickableListItem link="/database/bullet">Bullets</ClickableListItem>
          </CardList>
        </Col>
      </Row>
    )
  }
}
