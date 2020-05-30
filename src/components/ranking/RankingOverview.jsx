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
import { BLUE } from "../colors";
import Pagination from "../common/Pagination";
import OverviewFilter from "../database/OverviewFilter";
import { fetchRankingData } from "../fetch";
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

class RankingOverview extends React.Component {
  constructor(props) {
    super(props);

    this.initalFilterState = this.getInitalFilterState();

    const searchParams = new URLSearchParams(location.search);

    this.state = {
      isLoading: true,
      hasError: false,
      response: {},
      // filters
      page: searchParams.get("page") || this.initalFilterState.page,
      order: searchParams.get("order") || this.initalFilterState.order,
      sort: searchParams.get("sort") || this.initalFilterState.sort,
      filter: searchParams.get("filter") || this.initalFilterState.filter,
      search: searchParams.get("search") || this.initalFilterState.search,
    }

    this.changeState = this.changeState.bind(this);
    this.setPage = this.setPage.bind(this);
    this.fetchData = this.fetchData.bind(this);

    // Change page title
    document.title = "Guilds";
  }

  getInitalFilterState() {
    return {
      page: 1,
      order: "asc",
      sort: "avg_rank",
      filter: "all",
      search: "",
    }
  }

  fetchData() {
    // params to filter data
    const searchParams = new URLSearchParams({
      page: this.state.page,
      order: this.state.order,
      sort: this.state.sort,
      filter: this.state.filter,
      search: this.state.search,
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
    fetchRankingData(searchParams).then(fetchResponse => {
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
      isLoading,
      hasError,
      response,
      page,
      order,
      sort,
      filter,
      search,
    } = this.state;

    return (
      <>
        {isLoading && (
          <TopBarProgress />
        )}
        <OverviewFilter
          tablename="guild"
          changeState={this.changeState}
          order={order}
          sort={sort}
          filter={filter}
          search={search}
        />
        {(!isLoading && !hasError) && (
          <Grid>
            {response.items.map(guild => {
              return (
                <GridItem to={`/ranking/guild/${guild.name_hash}`}>
                  <GridItemContent>
                    <Name tablename="guild" data={guild} />
                    <SubsWrapper>
                      <span>Server: {guild.server}</span>
                      <span>Members: {guild.number_of_members}</span>
                      <span>Average Rank: ~{Math.round(guild.avg_rank, 2)}</span>
                    </SubsWrapper>
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
          <Ad slot="1765010914" />
        )}
      </>
    )
  }
}

export default RankingOverview;
