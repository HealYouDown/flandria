import AuthService from "./AuthService";

function fetchDetailedPageData(table, code, changeState) {
  let auth = new AuthService();

  auth.fetch("GET", `database/${table}/${code}`)
  .then(res => {
    if (res.error) {
      changeState({
        error: true,
        errorMessage: res.errorMessage
      })
    }
    else {
      changeState({
        loading: false,
        data: res.body
      })
    }
  })
}

export {
  fetchDetailedPageData,
}