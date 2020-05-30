import React from "react";
import TopBarProgress from "react-topbar-progress-indicator";
import { toast } from 'react-toastify';
import { fetchGuildData } from "../fetch";
import Ad from "../common/Ad";
import { Row, Col } from "react-grid-system";
import { Infos } from "../database/DetailedViewComponents"
import Card, { CardHeader, CardListBody } from "../common/Card";
import styled from "styled-components";
import Name from "../common/Name";

const ListItemWrapper = styled.li`
  display: flex;
  flex-flow: column;
  padding: 12px 20px;
`

const Sub = styled.span`
  font-size: 12px;
`

class RankingDetailedView extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      isLoading: true,
      hasError: false,
      response: {},
    }

    this.fetchData = this.fetchData.bind(this);
  }

  fetchData() {
    let res;
    fetchGuildData(this.props.match.params.hash).then(fetchResponse => {
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

  componentDidMount() {
    this.fetchData();
  }

  render() {
    const {
      isLoading,
      hasError,
      response,
    } = this.state;

    const itemInfos = [
      { label: "Server", value: response.server },
      { label: "Members", value: response.number_of_members },
      { label: "Average Rank", value: `~${Math.round(response.avg_rank, 2)}` },
    ]

    if (isLoading) {
      return <TopBarProgress />
    }

    document.title = response.name;

    return (
      <>
        <Row>
          <Col md={4}>
            <Infos tablename="guild" data={response} itemInfos={itemInfos} />
          </Col>
          <Col md={8}>
            <Card>
              <CardHeader>
                <span className="card-title">Members</span>
              </CardHeader>
              <CardListBody>
                <ul>
                  {response["members"].sort((a, b) => a.rank - b.rank).map(player => {
                    return (
                      <ListItemWrapper>
                        <Name tablename="player" data={player} />
                        <Sub>Class: {player.class}</Sub>
                        <Sub>Level: {player.level_land}/{player.level_sea}</Sub>
                        <Sub>Rank: {player.rank}</Sub>
                      </ListItemWrapper>
                    )
                  })}
                </ul>
              </CardListBody>
            </Card>
          </Col>
        </Row>
        <Ad slot="1765010914" />
      </>
    )
  }
}

export default RankingDetailedView;
