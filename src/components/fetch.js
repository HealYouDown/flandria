import { getToken } from "./auth/auth";

const getHeaders = () => {
  const token = getToken();
  let httpHeaders = {
    "Content-Type": "application/json",
    "Accept": "application/json",
  };

  if (token) {
    httpHeaders["Authorization"] = `Bearer ${token}`;
  }

  return new Headers(httpHeaders);
}

// API Functions
const fetchTabledata = (tablename, searchParams) => {
  const url = `/api/database/${tablename}?${searchParams.toString()}`;
  return fetch(url, {
    method: "GET",
    headers: getHeaders(),
  })
}

const fetchDetailedItemData = (tablename, itemCode) => {
  const url = `/api/database/${tablename}/${itemCode}`;
  return fetch(url, {
    method: "GET",
    headers: getHeaders(),
  });
}

const searchDatabase = (string) => {
  const url = `/api/search?s=${string}`;
  return fetch(url, {
    method: "GET",
    headers: getHeaders(),
  })
}

const changeDropQuantity = (dropId, newQuantity) => {
  const url = "/api/drops/edit";
  return fetch(url, {
    method: "PATCH",
    headers: getHeaders(),
    body: JSON.stringify({
      drop_id: dropId,
      new_quantity: newQuantity,
    })
  })
}

const deleteDrop = (dropId) => {
  const url = "/api/drops/delete";
  return fetch(url, {
    method: "DELETE",
    headers: getHeaders(),
    body: JSON.stringify({
      drop_id: dropId,
    })
  })
}

const addDrop = (monsterCode, itemCode) => {
  const url = "/api/drops/add";
  return fetch(url, {
    method: "POST",
    headers: getHeaders(),
    body: JSON.stringify({
      monster_code: monsterCode,
      item_code: itemCode
    })
  })
}

const getPlannerData = (class_) => {
  const url = "/api/planner/" + class_;
  return fetch(url, {
    method: "GET",
    headers: getHeaders(),
  })
}

const savePlannerBuild = (plannerClass, buildName, buildDescription, selectedLevel, selectedClass, hash) => {
  const url = `/api/planner/${plannerClass}/builds`;
  return fetch(url, {
    method: "PUT",
    headers: getHeaders(),
    body: JSON.stringify({
      build_name: buildName,
      build_description: buildDescription,
      selected_level: selectedLevel,
      selected_class: selectedClass,
      hash: hash,
    })
  })
}

const getPlannerBuilds = (plannerClass) => {
  const url = `/api/planner/${plannerClass}/builds`;
  return fetch(url, {
    method: "GET",
    headers: getHeaders(),
  })
}

const addStar = (buildId, userId) => {
  const url = `/api/planner/stars`;
  return fetch(url, {
    method: "PUT",
    headers: getHeaders(),
    body: JSON.stringify({
      user_id: userId,
      build_id: buildId,
    })
  })
}

const deleteStar = (buildId, userId) => {
  const url = `/api/planner/stars`;
  return fetch(url, {
    method: "DELETE",
    headers: getHeaders(),
    body: JSON.stringify({
      user_id: userId,
      build_id: buildId,
    })
  })
}

const getMapPoints = (mapCode) => {
  const url = `/api/map/${mapCode}`;
  return fetch(url, {
    method: "GET",
    headers: getHeaders(),
  });
}

export {
  fetchTabledata,
  fetchDetailedItemData,
  searchDatabase,
  changeDropQuantity,
  deleteDrop,
  addDrop,
  getPlannerData,
  savePlannerBuild,
  getPlannerBuilds,
  addStar,
  deleteStar,
  getMapPoints,
}