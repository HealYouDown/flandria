import React from "react";
import { fetchDetailedItemData } from "../fetch";
import TopBarProgress from "react-topbar-progress-indicator";
import { toast } from 'react-toastify';
import Monster from "./pages/Monster";
import WeaponAndArmor from "./pages/WeaponAndArmor";
import QuestItem from "./pages/QuestItem";
import QuestScroll from "./pages/QuestScroll";
import DressAndHat from "./pages/DressAndHat";
import Accessory from "./pages/Accessory";
import Recipe from "./pages/Recipe";
import Material from "./pages/Material";
import Production from "./pages/Production";
import ShipStuff from "./pages/ShipStuff";
import ShellAndShipFlag from "./pages/ShellAndShipFlag"
import PetCombineHelpAndStone from "./pages/PetCombineHelpAndStone";
import PetSkillStone from "./pages/PetSkillStone";
import RidingPet from "./pages/RidingPet";
import Pet from "./pages/Pet";
import Enhancing from "./pages/Enhancing";
import FishingRod from "./pages/FishingRod";
import FishingItem from "./pages/FishingItem";
import FishingBait from "./pages/FishingBait";
import RandomBox from "./pages/RandomBox";
import Consumable from "./pages/Consumable";
import Bullet from "./pages/Bullet";
import Quest from "./pages/Quest";
import Essence from "./pages/Essence";
import EssenceHelpItem from "./pages/EssenceHelpItem"

class DetailedView extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      isLoading: true,
      error: false,
      response: null,
      tablename: props.match.params.tablename,
      code: props.match.params.code,
    }

    this.fetchData = this.fetchData.bind(this);
  }

  fetchData() {
    let res;
    fetchDetailedItemData(this.state.tablename, this.state.code).then(fetchResponse => {
      res = fetchResponse;
      return fetchResponse.json()
    }).then(json => {
      if (!res.ok) {
        this.setState({error: true});
        toast.error(json.msg);
      } else {
        this.setState({response: json});
      }
      this.setState({isLoading: false});
    });
  }

  componentDidMount() {
    this.fetchData();
  }

  componentWillReceiveProps(nextProps) {
    this.setState({
      tablename: nextProps.match.params.tablename,
      code: nextProps.match.params.code,
      isLoading: true,
      response: null,
      error: false,
    }, () => {
      this.fetchData();
    })
  }

  render() {
    const {
      isLoading, error, response, tablename 
    } = this.state;

    if (isLoading) {
      return <TopBarProgress />
    }

    // changes page title
    if (tablename == "production") {
      document.title = response.obj.result_item.name
    } else {
      document.title = response.obj.name;
    }

    let detailedPage = null;
    const armorAndWeaponTables = ["cariad", "rapier", "dagger", "one_handed_sword", "two_handed_sword", "shield", "rifle", "duals", "coat", "pants", "gauntlet", "shoes"];
    const shipStuffTables = ["ship_body", "ship_front", "ship_head_mast", "ship_main_mast", "ship_figure", "ship_magic_stone", "ship_anchor", "ship_normal_weapon", "ship_special_weapon"];

    // kill me.
    if (tablename == "monster") {
      detailedPage = <Monster tablename={tablename} data={response} />;
    } else if (armorAndWeaponTables.includes(tablename)) {
      detailedPage = <WeaponAndArmor tablename={tablename} data={response} />;
    } else if (tablename == "quest_item") {
      detailedPage = <QuestItem tablename={tablename} data={response} />
    } else if (tablename == "quest_scroll") {
      detailedPage = <QuestScroll tablename={tablename} data={response} />
    } else if (["dress", "hat"].includes(tablename)) {
      detailedPage = <DressAndHat tablename={tablename} data={response} />
    } else if (tablename == "accessory") {
      detailedPage = <Accessory tablename={tablename} data={response} />
    } else if (tablename == "recipe") {
      detailedPage = <Recipe tablename={tablename} data={response} />
    } else if (tablename == "material") {
      detailedPage = <Material tablename={tablename} data={response} />
    } else if (tablename == "production") {
      detailedPage = <Production tablename={tablename} data={response} />
    } else if (shipStuffTables.includes(tablename)) {
      detailedPage = <ShipStuff tablename={tablename} data={response} />
    } else if (["ship_flag", "shell"].includes(tablename)) {
      detailedPage = <ShellAndShipFlag tablename={tablename} data={response} />
    } else if (["pet_combine_help", "pet_combine_stone"].includes(tablename)) {
      detailedPage = <PetCombineHelpAndStone tablename={tablename} data={response} />
    } else if (tablename == "pet_skill_stone") {
      detailedPage = <PetSkillStone tablename={tablename} data={response} />
    } else if (tablename == "pet") {
      detailedPage = <Pet tablename={tablename} data={response} />
    } else if (tablename == "riding_pet") {
      detailedPage = <RidingPet tablename={tablename} data={response} />
    } else if (["seal_break_help", "upgrade_help", "upgrade_crystal", "upgrade_stone"].includes(tablename)) {
      detailedPage = <Enhancing tablename={tablename} data={response} />
    } else if (tablename == "fishing_rod") {
      detailedPage = <FishingRod tablename={tablename} data={response} />
    } else if (tablename == "fishing_material") {
      detailedPage = <FishingItem tablename={tablename} data={response} />
    } else if (tablename == "fishing_bait") {
      detailedPage = <FishingBait tablename={tablename} data={response} />
    } else if (tablename == "random_box") {
      detailedPage = <RandomBox tablename={tablename} data={response} />
    } else if (tablename == "consumable") {
      detailedPage = <Consumable tablename={tablename} data={response} />
    } else if (tablename == "bullet") {
      detailedPage = <Bullet tablename={tablename} data={response} />
    } else if (tablename == "quest") {
      detailedPage = <Quest tablename={tablename} data={response} />
    } else if (tablename == "essence") {
      detailedPage = <Essence tablename={tablename} data={response} />
    } else if (tablename == "essence_help_item") {
      detailedPage = <EssenceHelpItem tablename={tablename} data={response} />
    }

    return detailedPage;
  }
}

export default DetailedView;