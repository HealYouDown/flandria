import {SecondJobType} from "@/gql/graphql"

import {ColsWrapper} from "@/components/cols-wrapper"
import {
  PageHeader,
  PageHeaderBreadcrumbs,
  PageTitle,
} from "@/components/page-header"
import {
  Card,
  CardContentList,
  CardDescription,
  CardHeader,
  CardTitle,
  CardContentLinkListItem as ListItem,
} from "@/components/ui/card"

import {createFileRoute} from "@tanstack/react-router"
import {
  BoxIcon,
  DiamondIcon,
  FishIcon,
  HammerIcon,
  PickaxeIcon,
  SailboatIcon,
  ScrollTextIcon,
  ShieldIcon,
  ShirtIcon,
  SquirrelIcon,
  SwordsIcon,
} from "lucide-react"

export const Route = createFileRoute("/database/")({
  component: DatabaseIndex,
})

const WeaponsSection = (
  <Card>
    <CardHeader>
      <div className="flex items-center gap-2">
        <SwordsIcon />
        <CardTitle>Weapons</CardTitle>
      </div>
      <CardDescription>
        Class-specific gear to help conquer fearsome foes.
      </CardDescription>
    </CardHeader>
    <CardContentList>
      <ListItem to="/database/cariad">Cariads</ListItem>
      <ListItem to="/database/rapier">Rapiers</ListItem>
      <ListItem to="/database/dagger">Daggers</ListItem>
      <ListItem to="/database/one_handed_sword">One-handed Swords</ListItem>
      <ListItem to="/database/two_handed_sword">Two-handed Swords</ListItem>
      <ListItem to="/database/shield">Shields</ListItem>
      <ListItem to="/database/rifle">Rifles</ListItem>
      <ListItem to="/database/duals">Duals</ListItem>
    </CardContentList>
  </Card>
)

const ArmorSection = (
  <Card>
    <CardHeader>
      <div className="flex items-center gap-2">
        <ShieldIcon />
        <CardTitle>Armor</CardTitle>
      </div>
      <CardDescription>
        Reliable gear that equips players for every challenge.
      </CardDescription>
    </CardHeader>
    <CardContentList>
      <ListItem to="/database/coat">Coats</ListItem>
      <ListItem to="/database/pants">Pants</ListItem>
      <ListItem to="/database/gauntlet">Gauntlets</ListItem>
      <ListItem to="/database/shoes">Shoes</ListItem>
    </CardContentList>
  </Card>
)

const ExtraEquipmentSection = (
  <Card>
    <CardHeader>
      <div className="flex items-center gap-2">
        <ShirtIcon />
        <CardTitle>Extra Equipment</CardTitle>
      </div>
      <CardDescription>
        Accessories that further enhance player stats.
      </CardDescription>
    </CardHeader>
    <CardContentList>
      <ListItem to="/database/hat">Hats</ListItem>
      <ListItem to="/database/dress">Dresses</ListItem>
      <ListItem to="/database/accessory">Accessories</ListItem>
    </CardContentList>
  </Card>
)

const QuestsSection = (
  <Card>
    <CardHeader>
      <div className="flex items-center gap-2">
        <ScrollTextIcon />
        <CardTitle>Quests</CardTitle>
      </div>
      <CardDescription>
        Epic journeys that offer treasures for the bold.
      </CardDescription>
    </CardHeader>
    <CardContentList>
      <ListItem to="/database/quest_scroll">Quest Scrolls</ListItem>
      <ListItem to="/database/quest_item">Quest Items</ListItem>
    </CardContentList>
  </Card>
)

const EssencesSection = (
  <Card>
    <CardHeader>
      <div className="flex items-center gap-2">
        <DiamondIcon />
        <CardTitle>Essences</CardTitle>
      </div>
      <CardDescription>
        Mystical infusions that elevate gear to new heights.
      </CardDescription>
    </CardHeader>
    <CardContentList>
      <ListItem to="/database/essence">Essences</ListItem>
      <ListItem to="/database/essence_help">Essence Help Items</ListItem>
      <ListItem
        to="/database/production"
        search={{type: SecondJobType.Essence}}
      >
        Essence Recipes
      </ListItem>
    </CardContentList>
  </Card>
)

const CraftingSection = (
  <Card>
    <CardHeader>
      <div className="flex items-center gap-2">
        <PickaxeIcon />
        <CardTitle>Crafting</CardTitle>
      </div>
      <CardDescription>
        The art of creating powerful gear from raw materials.
      </CardDescription>
    </CardHeader>
    <CardContentList>
      <ListItem to="/database/recipe">Recipes</ListItem>
      <ListItem to="/database/material">Materials</ListItem>
      <ListItem to="/database/production">Second Job</ListItem>
      <ListItem to="/database/production_book">2nd Job Books</ListItem>
    </CardContentList>
  </Card>
)

const ShipsSection = (
  <Card>
    <CardHeader>
      <div className="flex items-center gap-2">
        <SailboatIcon />
        <CardTitle>Ships</CardTitle>
      </div>
      <CardDescription>
        Essential upgrades to strengthen your vessel for the journey.
      </CardDescription>
    </CardHeader>
    <CardContentList>
      <ListItem to="/database/ship_body">Bodies</ListItem>
      <ListItem to="/database/ship_front">Fronts</ListItem>
      <ListItem to="/database/ship_head_mast">Head Masts</ListItem>
      <ListItem to="/database/ship_main_mast">Main Masts</ListItem>
      <ListItem to="/database/ship_figure">Figures</ListItem>
      <ListItem to="/database/ship_magic_stone">Magic Stones</ListItem>
      <ListItem to="/database/ship_anchor">Anchors</ListItem>
      <ListItem to="/database/ship_shell">Shells</ListItem>
      <ListItem to="/database/ship_flag">Flags</ListItem>
      <ListItem to="/database/ship_normal_weapon">Weapons</ListItem>
      <ListItem to="/database/ship_special_weapon">Special Weapons</ListItem>
    </CardContentList>
  </Card>
)

const PetsSection = (
  <Card>
    <CardHeader>
      <div className="flex items-center gap-2">
        <SquirrelIcon />
        <CardTitle>Pets</CardTitle>
      </div>
      <CardDescription>
        Loyal companions that aid in battle and gather loot.
      </CardDescription>
    </CardHeader>
    <CardContentList>
      <ListItem to="/database/pet">Pets</ListItem>
      <ListItem to="/database/riding_pet">Riding Pets</ListItem>
      <ListItem to="/database/pet_skill_stone">Pet Skill Stones</ListItem>
      <ListItem to="/database/pet_combine_stone">Combine Stones</ListItem>
      <ListItem to="/database/pet_combine_help">Combine Help Items</ListItem>
    </CardContentList>
  </Card>
)

const EnhancingSection = (
  <Card>
    <CardHeader>
      <div className="flex items-center gap-2">
        <HammerIcon />
        <CardTitle>Enhancing</CardTitle>
      </div>
      <CardDescription>Upgrade gear to boost its power.</CardDescription>
    </CardHeader>
    <CardContentList>
      <ListItem to="/database/seal_break_help">Seal Break Items</ListItem>
      <ListItem to="/database/upgrade_help">Upgrade Help Item</ListItem>
      <ListItem to="/database/upgrade_crystal">Upgrade Crystals</ListItem>
      <ListItem to="/database/upgrade_stone">Upgrade Stone</ListItem>
    </CardContentList>
  </Card>
)

const FishingSection = (
  <Card>
    <CardHeader>
      <div className="flex items-center gap-2">
        <FishIcon />
        <CardTitle>Fishing</CardTitle>
      </div>
      <CardDescription>Something seems fishy...</CardDescription>
    </CardHeader>
    <CardContentList>
      <ListItem to="/database/fishing_rod">Fishing Rods</ListItem>
      <ListItem to="/database/fishing_material">Fishing Materials</ListItem>
      <ListItem to="/database/fishing_bait">Fishing Baits</ListItem>
    </CardContentList>
  </Card>
)

const OtherSection = (
  <Card>
    <CardHeader>
      <div className="flex items-center gap-2">
        <BoxIcon />
        <CardTitle>More</CardTitle>
      </div>
      <CardDescription>Additional uncategorized items.</CardDescription>
    </CardHeader>
    <CardContentList>
      <ListItem to="/database/random_box">Random Boxes</ListItem>
      <ListItem to="/database/consumable">Consumables</ListItem>
      <ListItem to="/database/skill_book">Skill Books</ListItem>
      <ListItem to="/database/bullet">Bullets</ListItem>
    </CardContentList>
  </Card>
)

function DatabaseIndex() {
  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs
          items={[
            {label: "Home", href: "/"},
            {label: "Database", href: "/database"},
          ]}
        />
        <PageTitle title="Database" />
      </PageHeader>
      <ColsWrapper>
        <div>
          {WeaponsSection}
          {ArmorSection}
          {ExtraEquipmentSection}
          {QuestsSection}
        </div>
        <div>
          {EssencesSection}
          {CraftingSection}
          {ShipsSection}
        </div>
        <div>
          {PetsSection}
          {EnhancingSection}
          {FishingSection}
          {OtherSection}
        </div>
      </ColsWrapper>
    </>
  )
}
