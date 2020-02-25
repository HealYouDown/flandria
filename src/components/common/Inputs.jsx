import styled from "styled-components";
import { BLUE } from "../colors";

const InputWrapper = styled.div`
  display: flex;
  flex-flow: column;

  > label {
    margin-bottom: 3px;
  }

  > * {
    flex-grow: 1;
  }

  &:not(:first-child) {
    margin-top: 20px;
  }
`

const InputLabel = styled.label`
  color: white;
`;


const TextInput = styled.input`
  border: none;
  border-bottom: 2px solid #aaa;
  color: #aaa;
  background: transparent;
  font-size: ${props => props.fontsize}px;
  outline: none;
  box-shadow: none;

  &:focus {
    color: ${BLUE};
    border-bottom-color: ${BLUE};
  }

  &:invalid {
    border: none;
    border-bottom: 2px solid red;
  }
`;


const ConfirmButton = styled.button`
  border: none;
  border-radius: 3px;
  cursor: pointer;
  text-align: center;
  padding: 5px 10px;
  background-color: #28a745;
  color: white;
  transition: background-color 0.15s;

  &:hover {
    background-color: #218838;
  }
`;


export {
  InputLabel,
  InputWrapper,
  TextInput,
  ConfirmButton,
}