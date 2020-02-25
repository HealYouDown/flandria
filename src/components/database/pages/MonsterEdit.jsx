import React, { useState, useEffect } from "react";
import { Row, Col } from "react-grid-system";
import Card, { CardHeader, CardListBody } from "../../common/Card";
import TopBarProgress from "react-topbar-progress-indicator";
import { fetchDetailedItemData, changeDropQuantity, deleteDrop, addDrop } from "../../fetch";
import styled from "styled-components";
import Icon from "../../common/Icon";
import Name from "../../common/Name";
import { TextInput } from "../../common/Inputs";
import { Link } from "react-router-dom";
import { useDebouncedCallback } from "use-debounce";
import { toast } from "react-toastify";
import ItemSearch from "../../common/ItemSearch";


const DropItemWrapper = styled.li`
  display: flex;
  flex-flow: row;
  align-items: center;

  > div {
    flex-grow: 1;
    display: flex;
    flex-flow: column;
  }
`

const DeleteButton = styled.button`
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 4px;
  background-color: orangered;
  color: white;
  text-align: center;
  cursor: pointer;

  &:hover {
    background-color: red;
  }
`


const MonsterEdit = (props) => {
  const [drops, setDrops] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchDetailedItemData("monster", props.match.params.code)
      .then(res => res.json())
      .then(json => {
        setDrops(json.drops);
        setIsLoading(false);
      })
  }, [])  

  const [changeQuantity] = useDebouncedCallback((dropId, value) => {
    let newQuantity = parseInt(value);
    
    if (isNaN(newQuantity)) {
      return;
    }

    let res;
    changeDropQuantity(dropId, newQuantity)
      .then(fetchResponse => {
        res = fetchResponse;
        return fetchResponse.json();
      })
      .then(json => {
        if (!res.ok) {
          toast.error(json.msg);
        } else {
          toast.success(json.msg);
        }
      })
  }, 500);

  const onDeleteClick = (dropId) => {
    let res;
    deleteDrop(dropId)
    .then(fetchResponse => {
      res = fetchResponse;
      return fetchResponse.json();
    })
    .then(json => {
      if (!res.ok) {
        toast.error(json.msg);
      } else {
        toast.success(json.msg);
        const newDrops = drops.filter(drop => drop.id != dropId);
        setDrops(newDrops);
      }
    })
  }

  const onAddDrop = (item) => {
    const itemCode = item.code;
    const monsterCode = props.match.params.code;

    let res;
    addDrop(monsterCode, itemCode)
      .then(fetchResponse => {
        res = fetchResponse;
        return fetchResponse.json();
      })
      .then(json => {
        if (!res.ok) {
          toast.error(json.msg);
        } else {
          toast.success(json.msg);
          const newDrops = [...drops, json.drop];
          setDrops(newDrops);
        }
      })
  }

  if (isLoading) {
    return <TopBarProgress />
  }

  console.log(drops);

  return (
    <Row>
      <Col md={4}>
        <Card>
          <CardHeader>
            <span className="card-title">Drops</span>
          </CardHeader>
          <CardListBody>
            <ul>
              {drops.map(drop => {
                return (
                  <DropItemWrapper>
                    <Icon tablename={drop.item.table} icon={drop.item.icon} />
                    <div>
                      <Link style={{textDecoration: "none"}} to={`/database/${drop.item.table}/${drop.item.code}`}>
                        <Name tablename={drop.item.table} data={drop.item} />
                      </Link>
                      <div>
                        <span>Quantity: </span>
                        <TextInput
                          type="number"
                          onChange={e => changeQuantity(drop.id, e.target.value)}
                          fontsize={14}
                          defaultValue={drop.quantity}
                        />
                      </div>
                    </div>
                    <DeleteButton
                      onClick={() => onDeleteClick(drop.id)}
                    >
                      Del
                    </DeleteButton>
                  </DropItemWrapper>
                )
              })}
            </ul>
          </CardListBody>
        </Card>
      </Col>

      <Col md={8}>
        <ItemSearch
          callback={onAddDrop}
        />
      </Col>
    </Row>
  )
}

export default MonsterEdit;