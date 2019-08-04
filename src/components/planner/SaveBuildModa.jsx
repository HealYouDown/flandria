import React, { useState } from "react";
import ReactModal from "react-modal";
import "../../styles/modal.css";
import "../../styles/forms.css";
import AuthService from "../AuthService";

const SaveBuildModal = ({isOpen, onRequestClose, plannerClass, hash, selectedLevel, selectedClass}) => {
  const [buildTitle, setBuildTitle] = useState("");
  const [buildDescription, setBuildDescription] = useState("");
  const [isPublic, setIsPublic] = useState(true);
  const maxDescriptionChars = 200;
  const [charsLeft, setCharsLeft] = useState(maxDescriptionChars);
  const auth = new AuthService();

  const saveBuild = () => {
    auth.fetch("PUT", `planner/${plannerClass}/builds`, {
      body: {
        title: buildTitle,
        description: buildDescription,
        public: isPublic,
        hash: hash,
        selected_level: selectedLevel,
        selected_class: selectedClass,
      }
    })
    .then(res => {
      if (res.error) {
        alert(res.errorMessage)
      }
      else {
        onRequestClose();
      }
    })
  }

  const onDescriptionChange = (event) => {
    let value = event.target.value;
    if (value.length > maxDescriptionChars) {
      return;
    }

    setBuildDescription(value);
    setCharsLeft(maxDescriptionChars - value.length);
  }

  return (
    <ReactModal
      isOpen={isOpen}
      onRequestClose={onRequestClose}
      className="save-build-modal"
      overlayClassName="modal-overlay"
    >
      <form style={{display: "flex", flexDirection: "column", height: "100%"}} onSubmit={saveBuild}>

        <div className="form-input-group">
          <label className="form-input-label">Title</label>
          <input 
            className="form-input input-style" 
            type="text" value={buildTitle} 
            onChange={e => setBuildTitle(e.target.value)}
            placeholder="Build title like 'Ultra OP PvP Pirate'"
          />
        </div>

        <div className="form-input-group">
          <label className="form-input-label">Public</label>
          <input 
            type="checkbox" 
            checked={isPublic} onChange={e => setIsPublic(e.target.checked)}
          />
        </div>

        <div style={{display: "flex", flexDirection: "column", flexGrow: 1}} className="form-input-group">
          <label className="form-input-label">Description ({charsLeft} chars left)</label>
          <textarea 
            style={{flexGrow: 1}}
            className="form-input input-style"
            value={buildDescription} 
            onChange={onDescriptionChange}
            placeholder="Description what makes this build special. E.g. 'Assault Vermillion max op 10/10 exca build.'"
          />
        </div>

        <div className="form-input-group">
          <button type="submit">Save</button>
        </div>
      </form>
    </ReactModal>
  )
}

export default SaveBuildModal;