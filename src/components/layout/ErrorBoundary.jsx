import React from "react";
import { withRouter } from "react-router-dom";

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      hasError: false,
      errorMessage: "",
    }

    // Resets error on url change
    this.props.history.listen((location, action) => {
      if (this.state.hasError) {
        this.setState({
          hasError: false,
          errorMessage: ""
        });
      }
    })
  }

  componentDidCatch(error, info) {
    this.setState({ hasError: true, errorMessage: error.message });
  }

  render() {
    const {
      hasError,
      errorMessage
    } = this.state;

    if (hasError) {
      return (
        <h2 style={{color: "red"}}>{errorMessage}</h2>
      )
    }

    return this.props.children;
  }
}

export default withRouter(ErrorBoundary);