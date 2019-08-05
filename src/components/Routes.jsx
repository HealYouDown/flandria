import React from "react";
import { Switch, Route } from "react-router-dom";

import NoMatch from "./layout/NoMatch";

import Home from "./home/Home";
import Overview from "./database/overview/Overview";
import Login from "./auth/Login";
import Register from "./auth/Register";
import TableOverview from "./database/overview/TableOverview";
import Accessory from "./database/detailed_pages/Accessory";
import WeaponAndArmor from "./database/detailed_pages/WeaponAndArmor";
import QuestScroll from "./database/detailed_pages/QuestScroll";
import QuestItem from "./database/detailed_pages/QuestItem";
import DressAndHat from "./database/detailed_pages/DressAndHat";
import Recipe from "./database/detailed_pages/Recipe";
import Material from "./database/detailed_pages/Material";
import ProductBook from "./database/detailed_pages/ProductBook";
import ShipStuff from "./database/detailed_pages/ShipStuff";
import FlagAndShell from "./database/detailed_pages/FlagAndShell";
import PetCombineHelpItem from "./database/detailed_pages/PetCombineHelpItem";
import PetCombineStone from "./database/detailed_pages/PetCombineStone";
import PetSkillStone from "./database/detailed_pages/PetSkillStone";
import Pet from "./database/detailed_pages/Pets";
import RidingPet from "./database/detailed_pages/RidingPet";
import Enhancing from "./database/detailed_pages/Enhancing";
import FishingRod from "./database/detailed_pages/FishingRod";
import FishingBait from "./database/detailed_pages/FishingBait";
import RandomBox from "./database/detailed_pages/RandomBox";
import Consumable from "./database/detailed_pages/Consumable";
import Bullet from "./database/detailed_pages/Bullet";
import Monster from "./database/detailed_pages/Monser";
import Quest from "./database/detailed_pages/Quest";
import Planner from "./planner/Planner";
import PlannerBuilds from "./planner/PlannerBuilds";
import PrivacyPolicy from "./home/PrivacyPolicy";
import About from "./home/About";

const routes = (
  <Switch>
    
    <Route exact path="/" component={Home} />
    <Route path="/privacy-policy" component={PrivacyPolicy} />
    <Route path="/about" component={About} />

    <Route path="/auth/login" component={Login} />
    <Route path="/auth/register" component={Register} />

    <Route exact path="/database" component={Overview} />
    <Route exact path="/database/:table" component={TableOverview} />

    <Route path="/database/monster/:code" component={Monster} />
    <Route path="/database/quest/:code" component={Quest} />
    <Route path="/database/accessory/:code" component={Accessory} />
    <Route path="/database/cariad/:code" component={props => {
        return <WeaponAndArmor table="cariad" {...props} />
      }} 
    />
    <Route path="/database/rapier/:code" component={props => {
        return <WeaponAndArmor table="rapier" {...props} />
      }} 
    />
    <Route path="/database/dagger/:code" component={props => {
        return <WeaponAndArmor table="dagger" {...props} />
      }} 
    />
    <Route path="/database/one_handed_sword/:code" component={props => {
        return <WeaponAndArmor table="one_handed_sword" {...props} />
      }} 
    />
    <Route path="/database/two_handed_sword/:code" component={props => {
        return <WeaponAndArmor table="two_handed_sword" {...props} />
      }} 
    />
    <Route path="/database/shield/:code" component={props => {
        return <WeaponAndArmor table="shield" {...props} />
      }} 
    />
    <Route path="/database/rifle/:code" component={props => {
        return <WeaponAndArmor table="rifle" {...props} />
      }} 
    />
    <Route path="/database/duals/:code" component={props => {
        return <WeaponAndArmor table="duals" {...props} />
      }} 
    />
    <Route path="/database/coat/:code" component={props => {
        return <WeaponAndArmor table="coat" {...props} />
      }} 
    />
    <Route path="/database/pants/:code" component={props => {
        return <WeaponAndArmor table="pants" {...props} />
      }} 
    />
    <Route path="/database/gauntlet/:code" component={props => {
        return <WeaponAndArmor table="gauntlet" {...props} />
      }} 
    />
    <Route path="/database/shoes/:code" component={props => {
        return <WeaponAndArmor table="shoes" {...props} />
      }} 
    />
    <Route path="/database/quest_scroll/:code" component={QuestScroll} />
    <Route path="/database/quest_item/:code" component={QuestItem} />
    <Route path="/database/dress/:code" component={props => {
        return <DressAndHat table="dress" {...props} />
      }} 
    />
    <Route path="/database/hat/:code" component={props => {
        return <DressAndHat table="hat" {...props} />
      }} 
    />
    <Route path="/database/recipe/:code" component={Recipe} />
    <Route path="/database/material/:code" component={Material} />
    <Route path="/database/product_book/:code" component={ProductBook} />

    <Route path="/database/shell/:code" component={props => {
        return <FlagAndShell table="shell" {...props} />
      }} 
    />    
    <Route path="/database/ship_flag/:code" component={props => {
        return <FlagAndShell table="ship_flag" {...props} />
      }} 
    />  
    <Route path="/database/ship_anchor/:code" component={props => {
        return <ShipStuff table="ship_anchor" {...props} />
      }} 
    />
    <Route path="/database/ship_body/:code" component={props => {
        return <ShipStuff table="ship_body" {...props} />
      }} 
    />
    <Route path="/database/ship_figure/:code" component={props => {
        return <ShipStuff table="ship_figure" {...props} />
      }} 
    />
    <Route path="/database/ship_head_mast/:code" component={props => {
        return <ShipStuff table="ship_head_mast" {...props} />
      }} 
    />
    <Route path="/database/ship_main_mast/:code" component={props => {
        return <ShipStuff table="ship_main_mast" {...props} />
      }} 
    />
    <Route path="/database/ship_magic_stone/:code" component={props => {
        return <ShipStuff table="ship_magic_stone" {...props} />
      }} 
    />
    <Route path="/database/ship_front/:code" component={props => {
        return <ShipStuff table="ship_front" {...props} />
      }} 
    />
    <Route path="/database/ship_normal_weapon/:code" component={props => {
        return <ShipStuff table="ship_normal_weapon" {...props} />
      }} 
    />
    <Route path="/database/ship_special_weapon/:code" component={props => {
        return <ShipStuff table="ship_special_weapon" {...props} />
      }} 
    />
    <Route path="/database/pet_combine_help/:code" component={PetCombineHelpItem} />
    <Route path="/database/pet_combine_stone/:code" component={PetCombineStone} />
    <Route path="/database/pet_skill_stone/:code" component={PetSkillStone} />
    <Route path="/database/pet/:code" component={Pet} />
    <Route path="/database/riding_pet/:code" component={RidingPet} />

    <Route path="/database/seal_break_help/:code" component={props => {
        return <Enhancing table="seal_break_help" {...props} />
      }} 
    />
    <Route path="/database/upgrade_help/:code" component={props => {
        return <Enhancing table="upgrade_help" {...props} />
      }} 
    />
    <Route path="/database/upgrade_crystal/:code" component={props => {
        return <Enhancing table="upgrade_crystal" {...props} />
      }} 
    />
    <Route path="/database/upgrade_stone/:code" component={props => {
        return <Enhancing table="upgrade_stone" {...props} />
      }} 
    />
    <Route path="/database/fishing_rod/:code" component={FishingRod} />
    <Route path="/database/fishing_bait/:code" component={FishingBait} />
    <Route path="/database/random_box/:code" component={RandomBox} />
    <Route path="/database/consumable/:code" component={Consumable} />
    <Route path="/database/bullet/:code" component={Bullet} />

    <Route exact path="/planner/:class" component={Planner} />
    <Route exact path="/planner/:class/builds" component={PlannerBuilds} />
    <Route exact path="/account/builds" component={props => {
        return <PlannerBuilds allUserBuilds {...props} />
      }} 
    />
    <Route component={NoMatch} />
  
  </Switch>
)

export {
  routes
}