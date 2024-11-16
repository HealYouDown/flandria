// ChatGPT opop
export function getPaginationLabels(
  currentPage: number,
  totalPages: number,
  maxVisible: number = 7,
): (number | null)[] {
  // Ensure max_visible is at least 5 to accommodate 2 ends + 2 ellipses + current page
  maxVisible = Math.max(5, maxVisible)

  // If the total number of pages is less than or equal to max_visible, show all pages
  if (totalPages <= maxVisible) {
    return Array.from({length: totalPages}, (_, i) => i + 1)
  }

  // Start by initializing the pagination list
  const pagination: (number | null)[] = []

  // Always include the first page
  pagination.push(1)

  // Determine the range of page numbers to display around the current page
  const leftBound = Math.max(2, currentPage - 2) // 2 pages before the current
  const rightBound = Math.min(totalPages - 1, currentPage + 2) // 2 pages after the current

  // Insert ellipsis after first page if needed
  if (leftBound > 2) {
    pagination.push(null)
  }

  // Append the range of page numbers between the bounds
  for (let i = leftBound; i <= rightBound; i++) {
    pagination.push(i)
  }

  // Insert ellipsis before the last page if needed
  if (rightBound < totalPages - 1) {
    pagination.push(null)
  }

  // Always include the last page
  pagination.push(totalPages)

  return pagination
}
export function calculateLimitOffsetFromPage(
  page: number,
  itemsPerPage: number = 100,
) {
  return {
    offset: (page - 1) * itemsPerPage,
    limit: itemsPerPage,
  }
}
