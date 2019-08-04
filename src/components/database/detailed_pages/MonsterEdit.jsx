import { FaTrash } from "react-icons/fa";
import { Row, Col } from "react-grid-system";
import React from "react";
import ReactModal from "react-modal";

import AuthService from "../../AuthService";
import Icon from "../Icon";
import ItemSearch from "../../shared/ItemSearch";
import Name from "../Name";

import "../../../styles/modal.css";

ReactModal.setAppElement("#root");

export default class EditMonsterModal extends React.Component {
  constructor(props) {
    super(props);
    this.auth = new AuthService();

    this.changeState = this.props.changeState;
    this._deleteDrop = this._deleteDrop.bind(this);
    this._addDrop = this._addDrop.bind(this);
  }

  _displayErrorMessage(errorMessage) {
    alert(errorMessage);
  }

  _changeQuantity(itemCode, newQuantity) {
    let q = parseInt(newQuantity);
    if (isNaN(q)) {
      return;
    }

    this.props.data.drops.forEach(drop => {
      if (drop.item.code == itemCode) {
        drop.quantity = q;
      }
    });

    this.auth.fetch("PATCH", "drops", {
      body: {
        monster_code: this.props.data.code,
        item_code: itemCode,
        quantity: q,
      }
    })
    .then(res => {
      if (res.error) {
        this._displayErrorMessage(res.errorMessage);
      }
      else {
        this.changeState({data: this.props.data});
      }
    })
  }

  _addDrop(item) {
    const monsterCode = this.props.data.code;

    this.auth.fetch("PUT", "drops", {
      body: {
        monster_code: monsterCode,
        item_code: item.code,
      }
    })
    .then(res => {
      if (res.error) {
        alert(res.errorMessage);
      }
      else {
        let data = this.props.data;
        data.drops.push({
          quantity: 1,
          item: item,
        });
        this.setState({data});
      }
    })
  }

  _deleteDrop(itemCode) {
    const monsterCode = this.props.data.code;

    this.auth.fetch("DELETE", "drops", {
      body: {
        monster_code: monsterCode,
        item_code: itemCode
      }
    })
    .then(res => {
      if (res.error) {
        this._displayErrorMessage(res.errorMessage);
      }
      else {
        let data = this.props.data;
        data.drops = data.drops.filter(d => d.item.code != itemCode);
        this.changeState({data});
      }
    })
  }

  render() {
    const {
      data,
      modalOpen,
    } = this.props;

    const drops = data.drops;

    return (
      <ReactModal
        isOpen={modalOpen}
        onRequestClose={() => this.changeState({modalOpen: false})}
        className="modal"
        overlayClassName="modal-overlay"
      >
        <Row>

          <Col md={4}>
            <div>
              {drops.map((drop, i) => {
                return (
                  <div key={i} style={{display: "flex", marginBottom: "5px"}}>
                    <Icon table={drop.item.table} data={drop.item} />
                    <div>
                      <div style={{display: "flex", justifyContent: "space-between"}}>
                        <Name table={drop.item.table} data={drop.item} />
                        <FaTrash 
                          className="fa-icon"
                          onClick={() => this._deleteDrop(drop.item.code)}
                        />
                      </div>
                      <div>
                        <label>Quantity: </label>
                        <input 
                          className="input-style"
                          type="text"
                          defaultValue={drop.quantity}
                          onChange={e => this._changeQuantity(drop.item.code, e.target.value)}
                        />
                      </div>

                    </div>
                  </div>
                )
              })}
            </div>
          </Col>
          
          <Col md={8}>
            <ItemSearch clickAction={this._addDrop}/>
          </Col>

        </Row>
      </ReactModal>
    )
  }
}