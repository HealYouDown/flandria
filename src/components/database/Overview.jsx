import React from "react";
import TopBarProgress from "react-topbar-progress-indicator";
import { toast } from 'react-toastify';
import styled from "styled-components";
import breakpoint from "../breakpoint";
import { TileBase } from "../common/StyleMixins";
import RightArrow from "../common/RightArrow";
import Name from "../common/Name";
import { Link } from "react-router-dom";
import Icon from "../common/Icon";
import { tableToSubs } from "../subs";
import { getBonuses } from "../bonus_codes";
import { BLUE } from "../colors";
import Pagination from "../common/Pagination";
import OverviewFilter from "./OverviewFilter";
import { fetchTabledata } from "../fetch";
import { essenceEquipCodes } from "../essence_equip_codes";
import Ad from "../common/Ad";

const Grid = styled.div`
  display: grid;
  grid-column-gap: 30px;
  grid-row-gap: 20px;
  margin-top: 20px;
  padding: 0px 0px;
  ${breakpoint("sm")`
    grid-template-columns: 1fr;
  `}
  ${breakpoint("md")`
    grid-template-columns: 1fr 1fr;
    padding: 0px 15px;
    `}
  ${breakpoint("lg")`
    grid-template-columns: 1fr 1fr 1fr;
  `}
  ${breakpoint("xl")`
    grid-template-columns: 1fr 1fr 1fr 1fr;
  `}
`

const GridItem = styled(Link)`
  text-decoration: none;
  ${TileBase};
  display: flex;
`

const GridItemContent = styled.div`
  flex-grow: 1;
  display: flex;
  flex-flow: column;
  justify-content: center;
`

const SubsWrapper = styled.div`
  display: flex;
  flex-flow: column;
  
  * {
    font-size: 12px;
  }
`

const BonusSubsWrapper = styled.div`
  display: grid;
  grid-template-columns: repeat(2, auto);
  * {
    font-size: 12px;
    color: ${BLUE};
  }
`

const Subs = ({tablename, data}) => {
  const subs = tableToSubs[tablename];
  if (!subs) {
    return null;
  }

  if (tablename == "essence") {
    return (
      <SubsWrapper>
        <span>{data.core_essence ? "Core Essence" : "Meta Essence"}</span>
        <span>Level: {data.level}</span>
        <span>Equip: {essenceEquipCodes[data.equip]}</span>
      </SubsWrapper>
    )
  }

  return (
    <SubsWrapper>
      {Object.keys(subs).map(key => {
        const subDataKeys = subs[key];

        if (Array.isArray(subDataKeys)) {
          return (
            <span>
              {key}: {data[subDataKeys[0]]}/{data[subDataKeys[1]]}
            </span>
          )
        }
        else {
          return <span>{key}: {data[subDataKeys]}</span>
        }
      })}
    </SubsWrapper>
  )
}

const BonusSubs = ({data}) => {
  if (Object.is(data.bonus_code_1, undefined)) {
    return null;
  }

  return (
    <BonusSubsWrapper>
      {getBonuses(data).map(bonus => {
        if (bonus.operator == "*") {
          return (
            <span>
              {bonus.name}: {Math.round(bonus.value*100, 2)}%
            </span>
          )
        } else {
          return (
            <span>
              {bonus.name}: {bonus.operator}{bonus.value}
            </span>
          )
        }
      })}
    </BonusSubsWrapper>
  )
}

class Overview extends React.Component {
  constructor(props) {
    super(props);

    this.initalFilterState = this.getInitalFilterState(props.match.params.tablename);

    const searchParams = new URLSearchParams(location.search);

    this.state = {
      tablename: this.props.match.params.tablename,
      isLoading: true,
      hasError: false,
      response: {},
      // filters
      page: searchParams.get("page") || this.initalFilterState.page,
      order: searchParams.get("order") || this.initalFilterState.order,
      sort: searchParams.get("sort") || this.initalFilterState.sort,
      filter: searchParams.get("filter") || this.initalFilterState.filter,
      location: searchParams.get("location") || this.initalFilterState.location,
      search: searchParams.get("search") || this.initalFilterState.search,
      bonuses: searchParams.has("bonuses") ? JSON.parse(searchParams.get("bonuses")) : this.initalFilterState.bonuses,
    }

    this.changeState = this.changeState.bind(this);
    this.setPage = this.setPage.bind(this);
    this.fetchData = this.fetchData.bind(this);

    // Change page title
    const tableNameSplits = this.state.tablename.split("_");
    let title = "";
    tableNameSplits.forEach(s => {
      title += `${s.charAt(0).toUpperCase() + s.slice(1)} `;
    });
    document.title = title;
  }

  getInitalFilterState(tablename) {
    const initalOrderDesc = ["dress", "hat", "accessory", "recipe", "material", "random_box",
      "consumable"];

    return {
      page: 1,
      order: (initalOrderDesc.includes(tablename) ? "desc" : "asc"),
      sort: "added",
      filter: "all",
      location: "location:-1",
      search: "",
      bonuses: [],
    }
  }

  fetchData() {
    // params to filter data
    const searchParams = new URLSearchParams({
      page: this.state.page,
      order: this.state.order,
      sort: this.state.sort,
      filter: this.state.filter,
      location: this.state.location,
      search: this.state.search,
      bonuses: JSON.stringify(this.state.bonuses),
    });

    // Updates search params in browser url based on current state
    this.props.history.replace({
      search: "?" + searchParams.toString()
    });

    // inital fetch state
    this.setState({
      isLoading: true,
      hasError: false,
    });

    // fetch
    let res;
    fetchTabledata(this.state.tablename, searchParams).then(fetchResponse => {
      res = fetchResponse;
      return fetchResponse.json();
    }).then(json => {
      if (!res.ok) {
        this.setState({hasError: true});
        toast.error(json.msg);
      }
      else {
        this.setState({response: json});
      }
      this.setState({isLoading: false});
      window.scrollTo(0, 0);
    });
  }

  setPage(page) {
    // Set page gets its own function because it's called in a hook
    this.changeState({page: page});
  }

  changeState(newState) {
    /// Function that is called when any filter state change occures
    this.setState(newState, () => {
      this.fetchData();
    })
  }

  componentDidMount() {
    /// Fetches data when comp. is mounted
    this.fetchData();
  }

  componentWillReceiveProps(nextProps) {
    // Resets filters and fetches new data when table was changed
    if (this.state.tablename != nextProps.match.params.tablename) {
      const newState = Object.assign({}, this.getInitalFilterState(nextProps.match.params.tablename));
      newState.tablename = nextProps.match.params.tablename;

      this.setState(newState, () => {
        this.fetchData();
      });
    }
  }

  render() {
    const {
      tablename,
      isLoading,
      hasError,
      response,
      page,
      order,
      sort,
      filter,
      location,
      search,
      bonuses,
    } = this.state;

    return (
      <>
        {isLoading && (
          <TopBarProgress />
        )}
        <OverviewFilter
          tablename={tablename}
          changeState={this.changeState}
          order={order}
          sort={sort}
          filter={filter}
          location={location}
          search={search}
          bonuses={bonuses}
        />
        {(!isLoading && !hasError) && (
          <Grid>
            {response.items.map(item => {
              return (
                <GridItem to={`/database/${tablename}/${item.code}`}>
                  {tablename == "production" ? (
                    <Icon tablename={tablename} icon={item.result_item.icon} />
                  ) : (
                    <Icon tablename={tablename} icon={item.icon} />
                  )}
                  <GridItemContent>
                    <Name tablename={tablename} data={item} overview />
                    <Subs tablename={tablename} data={item} />
                    <BonusSubs data={item} />
                  </GridItemContent>
                  <RightArrow />
                </GridItem>
              )
            })}
          </Grid>
        )}
        {(!isLoading && !hasError && response.pagination.labels.length >= 2) && (
          <Pagination
            page={page}
            setPage={this.setPage}
            hasNext={response.pagination.has_next}
            hasPrevious={response.pagination.has_previous}
            labels={response.pagination.labels}
          />
        )}
        {(!isLoading && !hasError) && (
          <Ad slot="9331756778" />
        )}
      </>
    )
  }
}

export default Overview;
