import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Axios from 'axios';
import ReactDOMServer from 'react-dom/server';
import TopBarProgress from 'react-topbar-progress-indicator';
import { getApiUrl, setWindowTitle } from '../../../helpers';
import InformationWidget from './Widgets/InformationWidget';
import QuestsWidget from './Widgets/QuestsWidget';
import Grid, { Column } from '../../shared/Grid';
import DropsWidget from './Widgets/DropsWidget';
import { armorTables, shipTables, weaponTables } from '../../../constants';
import SkillWidget from './Widgets/SkillWidget';
import UpgradeWidget from './Widgets/UpgradeWidget';
import DroppedByWidget from './Widgets/DroppedByWidget';
import ProducedByWidget from './Widgets/ProducedByWidget';
import NeededForWidget from './Widgets/NeededForWidget';
import RandomBoxesWidget from './Widgets/RandomBoxesWidget';
import ItemSetWidget from './Widgets/ItemSetWidget';
import SoldByWidget from './Widgets/SoldByWidget';
import EffectStatsWidget from './Widgets/EffectStatsWidget';
import DescriptionWidget from './Widgets/DescriptionWidget';
import MaterialList from './Widgets/MaterialList';
import DetailedTableViewHeader from './DetailedTableViewHeader';
import ShipInformation from './Widgets/ShipInformation';
import RandomBoxContentWidget from './Widgets/RandomBoxContentWidget';
import NPCShopItemsWidget from './Widgets/NPCShopItemsWidget';
import QuestMissionsWidget from './Widgets/QuestMissionsWidget';
import QuestRewardsWidgets from './Widgets/QuestRewardsWidget';
import MonsterMapsWidget from './Widgets/MonsterMapsWidget';

const isEmptyComponent = (children) => !ReactDOMServer.renderToStaticMarkup(children);

const DetailedTableView = () => {
  const { tablename, code } = useParams();
  const [fetchResult, setFetchResult] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const url = `${getApiUrl()}/database/${tablename}/${code}`;
    const fetchData = async () => {
      const result = await Axios(url);
      setFetchResult({
        tablename,
        code,
        data: result.data,
      });
      setIsLoading(false);

      // Update window title
      let title = '';
      if (tablename === 'production') {
        title = result.data.result_item.name;
      } else if (tablename === 'quest') {
        title = result.data.title;
      } else {
        title = result.data.name;
      }
      setWindowTitle(title);
    };

    setIsLoading(true);
    fetchData();
  }, [tablename, code]);

  if (isLoading) return <TopBarProgress />;

  // If tablename and code do not match current fetched data, return nothing
  // Prevents rendering of the components below with new tablename but not he
  // new data
  if (fetchResult.tablename !== tablename && fetchResult.code !== code) {
    return null;
  }

  // Unpack data from fetch result
  const { data } = fetchResult;

  // Create all widgets that go onto the detailed page, based on the tablename.
  let widgetColumns;

  if (tablename === 'monster') {
    widgetColumns = (
      <>
        <Column md={4}>
          <InformationWidget tablename={tablename} obj={data} />
          <SkillWidget skills={data.skills} />
        </Column>
        {(data.quests.length > 0 || data.map_points.length > 0) && (
        <Column md={4}>
          <QuestsWidget quests={data.quests} />
          <MonsterMapsWidget
            monster={{
              name: data.name,
              icon: data.icon,
              level: data.level,
              area: data.area,
              rating: data.rating,
            }}
            mapPoints={data.map_points}
          />
        </Column>
        )}
        <Column md={((data.quests.length > 0 || data.map_points.length > 0)) ? 4 : 8}>
          <DropsWidget drops={data.drops} />
        </Column>
      </>
    );
  } else if (weaponTables.includes(tablename) || armorTables.includes(tablename) || tablename === 'fishing_rod') {
    const middleColumn = (
      <>
        {data.upgrade_rule && (
          <UpgradeWidget tablename={tablename} obj={data} upgradeData={data.upgrade_rule} />
        )}
        <EffectStatsWidget effects={data.effects} />
        <ItemSetWidget itemSet={data.item_set} />
      </>
    );

    let middleColumnEmpty;
    try {
      middleColumnEmpty = isEmptyComponent(middleColumn);
    } catch {
      middleColumnEmpty = false;
    }

    widgetColumns = (
      <>
        <Column md={4}>
          <InformationWidget tablename={tablename} obj={data} />
          <ProducedByWidget
            recipes={data.produced_by.recipe}
            productions={data.produced_by.second_job}
          />
          <NeededForWidget
            recipes={data.needed_for.recipe}
            productions={data.needed_for.second_job}
          />
        </Column>
        {!middleColumnEmpty && (
          <Column md={4}>
            {middleColumn}
          </Column>
        )}
        <Column md={middleColumnEmpty ? 8 : 4}>
          <RandomBoxesWidget boxes={data.random_boxes} />
          <SoldByWidget soldBy={data.sold_by} />
          <DroppedByWidget droppedBy={data.dropped_by} />
        </Column>
      </>
    );
  } else if (['dress', 'hat', 'accessory', 'essence'].includes(tablename)) {
    widgetColumns = (
      <>
        <Column md={4}>
          <InformationWidget tablename={tablename} obj={data} />
        </Column>
        <Column md={4}>
          <EffectStatsWidget effects={data.effects} />
          {data.produced_by && (
            <ProducedByWidget
              recipes={data.produced_by.recipe}
              productions={data.produced_by.second_job}
            />
          )}
          {data.needed_for && (
            <NeededForWidget
              recipes={data.needed_for.recipe}
              productions={data.needed_for.second_job}
            />
          )}
        </Column>
        <Column md={4}>
          <RandomBoxesWidget boxes={data.random_boxes} />
          <DroppedByWidget droppedBy={data.dropped_by} />
        </Column>
      </>
    );
  } else if (tablename === 'quest_scroll') {
    widgetColumns = (
      <>
        <Column md={4}>
          <InformationWidget tablename={tablename} obj={data} />
        </Column>
        {data.quest && (
          <Column md={4}>
            <QuestsWidget quests={[data.quest]} />
          </Column>
        )}
        <Column md={data.quest ? 4 : 8}>
          <SoldByWidget soldBy={data.sold_by} />
          <DroppedByWidget droppedBy={data.dropped_by} />
        </Column>
      </>
    );
  } else if (tablename === 'quest_item') {
    widgetColumns = (
      <>
        <Column md={4}>
          <InformationWidget tablename={tablename} obj={data} />
        </Column>
        {data.quests && (
          <Column md={4}>
            <QuestsWidget quests={data.quests} />
          </Column>
        )}
        <Column md={data.quests ? 4 : 8}>
          <DroppedByWidget droppedBy={data.dropped_by} />
        </Column>
      </>
    );
  } else if (tablename === 'essence_help') {
    widgetColumns = (
      <>
        <Column md={4}>
          <InformationWidget tablename={tablename} obj={data} />
          <DescriptionWidget description={data.description} />
        </Column>
        <Column md={8}>
          <DroppedByWidget droppedBy={data.dropped_by} />
          <ProducedByWidget
            recipes={data.produced_by.recipe}
            productions={data.produced_by.second_job}
          />
          <NeededForWidget
            recipes={data.needed_for.recipe}
            productions={data.needed_for.second_job}
          />
          <RandomBoxesWidget boxes={data.random_boxes} />
        </Column>
      </>
    );
  } else if (['recipe', 'production'].includes(tablename)) {
    widgetColumns = (
      <>
        <Column md={4}>
          <InformationWidget tablename={tablename} obj={data} />
          {tablename === 'recipe' && (
            <>
              <RandomBoxesWidget boxes={data.random_boxes} />
              <SoldByWidget soldBy={data.sold_by} />
              <DroppedByWidget droppedBy={data.dropped_by} />
            </>
          )}
        </Column>
        <Column md={8}>
          <MaterialList
            resultItem={data.result_item}
            materials={data.materials}
          />
          {data.premium_essence_production && (
            <MaterialList
              label="[Premium] Materials"
              materials={data.premium_essence_production.materials}
              showResultItem={false}
            />
          )}
        </Column>
      </>
    );
  } else if (tablename === 'material') {
    widgetColumns = (
      <>
        <Column md={4}>
          <InformationWidget tablename={tablename} obj={data} />
          <RandomBoxesWidget boxes={data.random_boxes} />
          <SoldByWidget soldBy={data.sold_by} />
        </Column>
        <Column md={4}>
          <DroppedByWidget droppedBy={data.dropped_by} />
        </Column>
        <Column md={4}>
          <ProducedByWidget
            recipes={data.produced_by.recipe}
            productions={data.produced_by.second_job}
          />
          <NeededForWidget
            recipes={data.needed_for.recipe}
            productions={data.needed_for.second_job}
          />
        </Column>
      </>
    );
  } else if (tablename === 'product_book') {
    widgetColumns = (
      <>
        <Column md={4}>
          <InformationWidget tablename={tablename} obj={data} />
        </Column>
        <Column md={8}>
          <SoldByWidget soldBy={data.sold_by} />
        </Column>
      </>
    );
  } else if (shipTables.includes(tablename)) {
    widgetColumns = (
      <>
        <Column md={4}>
          <InformationWidget tablename={tablename} obj={data} />
        </Column>
        <Column md={4}>
          <ShipInformation tablename={tablename} obj={data} />
          <SoldByWidget soldBy={data.sold_by} />
        </Column>
        <Column md={4}>
          <ProducedByWidget
            recipes={data.produced_by.recipe}
            productions={data.produced_by.second_job}
          />
          <NeededForWidget
            recipes={data.needed_for.recipe}
            productions={data.needed_for.second_job}
          />
          <RandomBoxesWidget boxes={data.random_boxes} />
          <DroppedByWidget droppedBy={data.dropped_by} />
        </Column>
      </>
    );
  } else if (['ship_shell', 'ship_flag'].includes(tablename)) {
    widgetColumns = (
      <>
        <Column md={4}>
          <InformationWidget tablename={tablename} obj={data} />
        </Column>
        <Column md={8}>
          <SoldByWidget soldBy={data.sold_by} />
          <DroppedByWidget droppedBy={data.dropped_by} />
        </Column>
      </>
    );
  } else if (['pet_combine_help', 'pet_combine_stone'].includes(tablename)) {
    widgetColumns = (
      <>
        <Column md={4}>
          <InformationWidget tablename={tablename} obj={data} />
        </Column>
        <Column md={8}>
          <RandomBoxesWidget boxes={data.random_boxes} />
          <DroppedByWidget droppedBy={data.dropped_by} />
        </Column>
      </>
    );
  } else if (tablename === 'pet_skill_stone') {
    widgetColumns = (
      <>
        <Column md={4}>
          <InformationWidget tablename={tablename} obj={data} />
        </Column>
        <Column md={4}>
          <SkillWidget skills={[data.skill]} />
        </Column>
        <Column md={4}>
          <RandomBoxesWidget boxes={data.random_boxes} />
          <DroppedByWidget droppedBy={data.dropped_by} />
        </Column>
      </>
    );
  } else if (tablename === 'pet') {
    widgetColumns = (
      <>
        <Column md={4}>
          <InformationWidget tablename={tablename} obj={data} />
        </Column>
        <Column md={8}>
          <RandomBoxesWidget boxes={data.random_boxes} />
          <DroppedByWidget droppedBy={data.dropped_by} />
        </Column>
      </>
    );
  } else if (['riding_pet', 'seal_break_help', 'upgrade_help', 'upgrade_crystal', 'upgrade_stone'].includes(tablename)) {
    widgetColumns = (
      <>
        <Column md={4}>
          <InformationWidget tablename={tablename} obj={data} />
        </Column>
        {data.description && (
          <Column md={4}>
            <DescriptionWidget description={data.description} />
          </Column>
        )}
        <Column md={data.description ? 4 : 8}>
          {data.sold_by && (
            <SoldByWidget soldBy={data.sold_by} />
          )}
          <RandomBoxesWidget boxes={data.random_boxes} />
          {data.dropped_by && (
            <DroppedByWidget droppedBy={data.dropped_by} />
          )}
        </Column>
      </>
    );
  } else if (tablename === 'fishing_material') {
    widgetColumns = (
      <>
        <Column md={4}>
          <InformationWidget tablename={tablename} obj={data} />
        </Column>
        <Column md={4}>
          <SoldByWidget soldBy={data.sold_by} />
          <RandomBoxesWidget boxes={data.random_boxes} />
          <DroppedByWidget droppedBy={data.dropped_by} />
        </Column>
        <Column md={4}>
          <ProducedByWidget
            recipes={data.produced_by.recipe}
            productions={data.produced_by.second_job}
          />
          <NeededForWidget
            recipes={data.needed_for.recipe}
            productions={data.needed_for.second_job}
          />
        </Column>
      </>
    );
  } else if (tablename === 'random_box') {
    widgetColumns = (
      <>
        <Column md={4}>
          <InformationWidget tablename={tablename} obj={data} />
          <ProducedByWidget
            recipes={data.produced_by.recipe}
            productions={data.produced_by.second_job}
          />
          <NeededForWidget
            recipes={data.needed_for.recipe}
            productions={data.needed_for.second_job}
          />
        </Column>
        <Column md={4}>
          <SoldByWidget soldBy={data.sold_by} />
          <RandomBoxesWidget boxes={data.random_boxes} />
          <DroppedByWidget droppedBy={data.dropped_by} />
        </Column>
        <Column md={4}>
          <RandomBoxContentWidget items={data.items} />
        </Column>
      </>
    );
  } else if (tablename === 'consumable') {
    widgetColumns = (
      <>
        <Column md={4}>
          <InformationWidget tablename={tablename} obj={data} />
          <ProducedByWidget
            recipes={data.produced_by.recipe}
            productions={data.produced_by.second_job}
          />
          <NeededForWidget
            recipes={data.needed_for.recipe}
            productions={data.needed_for.second_job}
          />
        </Column>
        {data.description && (
          <Column md={4}>
            <DescriptionWidget description={data.description} />
          </Column>
        )}
        <Column md={data.description ? 4 : 8}>
          <RandomBoxesWidget boxes={data.random_boxes} />
          <SoldByWidget soldBy={data.sold_by} />
          <DroppedByWidget droppedBy={data.dropped_by} />
        </Column>
      </>
    );
  } else if (['skill_book', 'fishing_bait', 'bullet'].includes(tablename)) {
    widgetColumns = (
      <>
        <Column md={4}>
          <InformationWidget tablename={tablename} obj={data} />
        </Column>
        <Column md={8}>
          <SoldByWidget soldBy={data.sold_by} />
          {data.dropped_by && (
            <DroppedByWidget droppedBy={data.dropped_by} />
          )}
        </Column>
      </>
    );
  } else if (tablename === 'npc') {
    widgetColumns = (
      <>
        <Column md={4}>
          <InformationWidget tablename={tablename} obj={data} />
        </Column>
        <Column md={8}>
          <NPCShopItemsWidget items={data.shop_items} />
        </Column>
      </>
    );
  } else if (tablename === 'quest') {
    const description = data.descriptions.en;

    widgetColumns = (
      <>
        <Column md={4}>
          <InformationWidget tablename={tablename} obj={data} />
          {data.before_quest && (
            <QuestsWidget label="Before Quest" quests={[data.before_quest]} />
          )}
          {data.after_quest && (
            <QuestsWidget label="After Quest" quests={[data.after_quest]} />
          )}
        </Column>
        <Column md={4}>
          <QuestMissionsWidget
            missions={data.missions}
            missionDescriptions={description.missions}
            giveItems={data.give_items}
          />
          <QuestRewardsWidgets
            rewards={data.selectable_items}
            selectCount={data.selectable_items_count}
          />
        </Column>
        <Column md={4}>
          <DescriptionWidget label="Description" description={description.description} />
          <DescriptionWidget label="Pre Dialog" description={description.pre_dialog} />
          <DescriptionWidget label="Start Dialog" description={description.start_dialog} />
          <DescriptionWidget label="Run Dialog" description={description.run_dialog} />
          <DescriptionWidget label="Finish Dialog" description={description.finish_dialog} />
        </Column>
      </>
    );
  }

  return (
    <>
      <DetailedTableViewHeader
        tablename={tablename}
        item={data}
      />
      <Grid className="mt-3">
        {widgetColumns}
      </Grid>
    </>
  );
};

export default DetailedTableView;
