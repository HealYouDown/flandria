// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-nocheck
// Due to tanstack routers search requiring a "from" parameter for a global
// component, and our database table not needing pages on all sub-sections,
// we just disable the ts-error we get for this file.
import {getPaginationLabels} from "@/utils/pagination"

import {
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
  Pagination as ShadeCnPagination,
} from "@/components/ui/pagination"

type PaginationProps = {
  currentPage: number
  totalItemsCount: number
  perPage: number
}

export function Pagination({
  currentPage,
  totalItemsCount,
  perPage,
}: PaginationProps) {
  const totalPageCount = Math.ceil(totalItemsCount / perPage)
  const labels = getPaginationLabels(currentPage, totalPageCount)

  const hasPrevious = currentPage > 1
  const hasNext = currentPage < totalPageCount

  return (
    <ShadeCnPagination>
      <PaginationContent>
        <PaginationItem>
          <PaginationPrevious
            disabled={!hasPrevious}
            className={hasPrevious ? "" : "cursor-not-allowed"}
            to="."
            search={(prev) => ({...prev, page: currentPage - 1})}
          />
        </PaginationItem>

        {labels.map((pageNum) => (
          <PaginationItem key={pageNum}>
            {pageNum === null ? (
              <PaginationEllipsis />
            ) : (
              <PaginationLink
                isActive={currentPage == pageNum}
                to="."
                search={(prev) => ({...prev, page: pageNum})}
              >
                {pageNum}
              </PaginationLink>
            )}
          </PaginationItem>
        ))}

        <PaginationItem>
          <PaginationNext
            disabled={!hasNext}
            className={hasNext ? "" : "cursor-not-allowed"}
            to="."
            search={(prev) => ({...prev, page: currentPage + 1})}
          />
        </PaginationItem>
      </PaginationContent>
    </ShadeCnPagination>
  )
}
