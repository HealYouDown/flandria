import React from "react";
import AuthService from "../AuthService";
import {Link} from "react-router-dom";
import RightArrow from "../shared/RightArrow";

import "./PlannerBuild.css";
import { FaStar, FaTrash } from "react-icons/fa";

export default class PlannerBuilds extends React.Component {
  constructor(props) {
    super(props);
    this.plannerClass = this.props.match.params.class || "all";
    this.allUserBuilds = this.props.allUserBuilds || false;
    this.auth = new AuthService();

    this.state = {
      loading: true,
      data: [],
      error: false,
      errorMessage: "",
    }
  }

  componentDidMount() {
    const url = `planner/${this.plannerClass}/builds`
    let options = {};
    if (this.allUserBuilds) {
      options.query = `allUserBuilds=1`
    }
    this.auth.fetch("GET", url, options)
    .then(res => {
      if (res.error) {
        this.setState({error: true, errorMessage: res.errorMessage});
      }
      else {
        this.setState({loading: false, data: res.body});
      }
    })
  }

  _addVote(e, buildId) {
    e.preventDefault();
    const userId = this.auth.getId();

    this.auth.fetch("PUT", `planner/${this.plannerClass}/builds/${buildId}/stars`, {
      body: {user_id: userId}
    })
      .then(res => {
        if (res.error) {
          this.setState({error: true, errorMessage: res.errorMessage})
        }
        else {
          let data = Object.assign([], this.state.data);
          let build = data.filter(d => d.index == buildId)[0];
          build.stars.push({
            user_id: userId,
            build_id: buildId,
          })
          this.setState({data})
        }
      })
  }

  _removeVote(e, buildId) {
    e.preventDefault();
    this.auth.fetch("DELETE", `planner/${this.plannerClass}/builds/${buildId}/stars`)
      .then(res => {
        if (res.error) {
          this.setState({error: true, errorMessage: res.errorMessage})
        }
        else {
          const userId = this.auth.getId();
          let data = Object.assign([], this.state.data);
          let build = data.filter(d => d.index == buildId)[0];
          build.stars = build.stars.filter(s => s.user_id != userId);
          this.setState({data})
        }
      })
   }

   _deleteBuild(e, buildId) {
     e.preventDefault();
     this.auth.fetch("DELETE", `planner/${this.plannerClass}/builds/${buildId}`)
     .then(res => {
      if (res.error) {
        this.setState({error: true, errorMessage: res.errorMessage})
      }
      else {
        let data = Object.assign([], this.state.data);
        data = data.filter(d => d.index != buildId);
        this.setState({data})
      }
    })
   }

  render() {
    const {
      loading,
      data,
      error,
      errorMessage,
    } = this.state;

    if (error) {
      throw Error(errorMessage);
    }

    if (loading) {
      return null;
    }

    let sortedBuilds = Object.assign([], data);
    sortedBuilds = sortedBuilds.sort((a, b) => a.stars.length < b.stars.length )

    return (
      <div className="list-wrapper">
          {sortedBuilds.map((build, index) => {
            let hasVoted = false;
            let canVote = false;

            if (this.auth.loggedIn()) {
              canVote = true;

              if (build.stars.some(star => {
                if (star.user_id == this.auth.getId()) {
                  return true;
                }
                return false;
              })) {
                hasVoted = true;
              }
            }

            let starClassName = hasVoted ? "star voted " : "star not-voted ";
            if (!canVote) {
              starClassName += " can-not-vote"
            }

            return (
              <div key={index} className="table-overview-list-item">
                <Link className="table-overview-list-item-inner" to={`/planner/${build.class_}#${build.hash}`}>
                  <div className="center">
                    
                    <div className="skill-build-header">
                      <span>{build.title}</span>
                      <div className="skill-build-header-right">
                        <div>
                          <FaStar
                            onClick={e => hasVoted ? this._removeVote(e, build.index) : this._addVote(e, build.index)}
                            className={starClassName}
                          />
                          <span>{build.stars.length}</span>
                        </div>
                        {(this.auth.loggedIn() && build.user.id == this.auth.getId()) && (
                          <div>
                            <FaTrash className="fa-icon" onClick={e => this._deleteBuild(e, build.index)} />
                          </div>
                        )}
                      </div>
                    </div>

                    <div className="skill-build-main">
                      <p className="skill-build-description">{build.description}</p>                      
                    </div>

                    <div className="skill-build-footer">
                      <span>by {build.user.username}, {new Date(build.time).toLocaleDateString()}</span>
                    </div>

                  </div>
                  <RightArrow />
                </Link>
              </div>
            )
          })}
      </div>
    )
  }
}