import React from "react";
import styled from "styled-components";
import { BLUE } from "../colors";
import { Link } from "react-router-dom";

const PaginationWrapper = styled.div`
  margin-top: 20px;
  display: flex;
  justify-content: center;
`

const PageButton = styled.button`
  color: ${props => props.active ? BLUE : "#aaa"};
  border: 1px solid black;
  background: rgba(0, 0, 0, 0.7);
  font-size: 14px;
  padding: 10px 15px;
  text-decoration: none;
  cursor: ${props => props.disabled ? "not-allowed" : "pointer"};

  &:hover {
    background: rgba(0, 0, 0, 0.9);
  }
`

const PageButtonWrapper = styled.div`
  display: flex;
  flex-flow: row wrap;
  justify-content: center;
`

const Pagination = ({page, setPage, hasNext, hasPrevious, labels}) => {
  return (
    <PaginationWrapper>
      <PageButtonWrapper>
        <PageButton
          disabled={!hasPrevious}
          onClick={e => {
            if (!hasPrevious) {
              e.preventDefault();
            }
            setPage(page-1);
          }}
        >
          «
        </PageButton>
        {labels.map(label => {
          if (label === null) {
            return (
              <PageButton onClick={e => e.preventDefault()}>…</PageButton>
            )
          }
          const pageNum = parseInt(label);
          return (
            <PageButton
              onClick={() => setPage(pageNum)}
              active={page == pageNum}
            >
              {label}
            </PageButton>
          )
        })}
        <PageButton
          disabled={!hasNext}
          onClick={e => {
            if (!hasNext) {
              e.preventDefault();
            }
            setPage(page+1);
          }}
        >
          »
        </PageButton>
      </PageButtonWrapper>
    </PaginationWrapper>
  )
}

export default Pagination;