import React from 'react';

const PageButton = ({
  children, isCurrent, disabled = false, onClick,
}) => (
  <button
    className={`${isCurrent ? 'text-gray-900 dark:text-dark-primary' : ''} ${disabled ? 'cursor-not-allowed' : 'cursor-pointer'} flex items-center text-lg justify-center border-2 dark:text-white border-gray-200 dark:border-dark-4 rounded-lg text-gray-500 font-semibold tabular-nums w-10 h-10 hover:bg-gray-200 dark:hover:bg-dark-3 hover:text-gray-700`}
    type="button"
    onClick={onClick}
    disabled={disabled}
  >
    {children}
  </button>
);

const Pagination = ({
  currentPage, hasPrevious, hasNext, labels, onPageChange,
}) => (
  <div className="flex flex-wrap justify-center gap-1 py-2">
    <PageButton
      key="left-pagination-btn"
      disabled={!hasPrevious}
      onClick={() => onPageChange(currentPage - 1)}
    >
      «
    </PageButton>
    {labels.map((label) => {
      if (label) {
        return (
          <PageButton
            key={label}
            isCurrent={parseInt(label, 10) === currentPage}
            onClick={() => onPageChange(parseInt(label, 10))}
          >
            {label}
          </PageButton>
        );
      }
      return (
        <PageButton
          key="center-pagination-btn"
          onClick={(event) => event.preventDefault()}
        >
          …
        </PageButton>
      );
    })}
    <PageButton
      key="right-pagination-btn"
      disabled={!hasNext}
      onClick={() => onPageChange(currentPage + 1)}
    >
      »
    </PageButton>
  </div>
);

export default Pagination;
