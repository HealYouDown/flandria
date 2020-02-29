import React, { useState, useEffect } from "react";
import { TileBase } from "../common/StyleMixins";
import RightArrow from "../common/RightArrow";
import styled from "styled-components";
import TopBarProgress from "react-topbar-progress-indicator";
import { getPlannerBuilds, deleteStar, addStar } from "../fetch";
import breakpoint from "../breakpoint";
import { Link } from "react-router-dom";
import { isLoggedIn, getId } from "../auth/auth";
import { BLUE } from "../colors";

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
  margin-right: 5px;
`

const BuildTitleWrapper = styled.div`
  display: flex;
  flex-flow: row;
  justify-content: space-between;
`

const BuildTitle = styled.span`
  font-size: 17px;
  font-weight: 700;
`

const BuildStarsCountWrapper = styled.div`
  display: flex;
  flex-flow: row;
  align-items: center;

  span:first-child {
    font-size: 22px;
  }

  span:last-child {
    font-size: 18px;
  }
`

const StarWrapper = styled.span`
  ${props => props.canBeVoted
    ? `
      color: ${props.isVotedByUser ? BLUE : "inherit"}
      &:hover {
        color: ${props.isVotedByUser ? "orangered" : BLUE};
      }
    `
    : ""
  }
`

const BuildDescription = styled.p`
  font-size: 14px;
`

const BuildFooter = styled.div`
  display: flex;
  flex-flow: row;
  justify-content: space-between;
  
  span {
    font-size: 11px;
  }
`

const BuildStats = styled.div`
  display: flex;
  flex-flow: column;

  span {
    font-size: 12px;
  }
`

const Builds = (props) => {
  const [isLoading, setIsLoading] = useState(true);
  const [builds, setBuilds] = useState([]);

  useEffect(() => {
    setIsLoading(true);

    getPlannerBuilds(props.match.params.plannerClass)
      .then(res => res.json())
      .then(json => {
        setBuilds(json);
        setIsLoading(false);
      })
  }, [props])

  const onStarClick = (event, build, isVotedByUser) => {
    event.preventDefault();
    const userId = getId();
  
    const buildsCopy = builds.filter(b => b.id != build.id);

    if (isVotedByUser) {
      // remove star
      let newStars = build.stars.filter(star => star.user_id != userId);
      build.stars = newStars;
      buildsCopy.push(build);

      deleteStar(build.id, userId);

    } else {
      // add star
      let newStars = build.stars;
      newStars.push({
        build_id: build.id,
        user_id: userId,
      })
      build.stars = newStars;
      buildsCopy.push(build);

      addStar(build.id, userId);
    }

    setBuilds(buildsCopy);
  }

  if (isLoading) {
    return <TopBarProgress />;
  }


  const sortedBuilds = builds.sort((a, b) => b.stars.length - a.stars.length);

  if (sortedBuilds.length == 0) {
    return <span>No builds found.</span>
  }

  return (
    <Grid>
      {sortedBuilds.map(build => {
        const date = new Date(build.created_at);
        date.setMinutes(date.getMinutes() - date.getTimezoneOffset())
        const dateString = date.toLocaleString();

        const userId = getId();
        const canBeVoted = isLoggedIn();
        let isVotedByUser = false;

        if (isLoggedIn()) {
          build.stars.forEach(star => {
            if (star.user_id == userId) {
              isVotedByUser = true;
            }
          })
        }

        return (
          <GridItem to={`/planner/${props.match.params.plannerClass}#${build.hash}`}>
            <GridItemContent>

              <BuildTitleWrapper>
                <BuildTitle>{build.build_name}</BuildTitle>
                <BuildStarsCountWrapper>
                  <StarWrapper
                    canBeVoted={canBeVoted}
                    isVotedByUser={isVotedByUser}
                    onClick={event => onStarClick(event, build, isVotedByUser)}
                  >
                    ★
                  </StarWrapper>
                  <span>{build.stars.length}</span>
                </BuildStarsCountWrapper>
              </BuildTitleWrapper>

              <BuildStats>
                {build.selected_class != null && (
                  <span>Class: {build.selected_class}</span>
                )}
                <span>Level: {build.selected_level}</span>
              </BuildStats>

              <BuildDescription>
                {build.build_description}
              </BuildDescription>

              <BuildFooter>
                <span>By {build.user.username}</span>
                <span>{dateString}</span>
              </BuildFooter>

            </GridItemContent>
            <RightArrow />
          </GridItem>
        )
      })}
    </Grid>
  )

}

export default Builds;