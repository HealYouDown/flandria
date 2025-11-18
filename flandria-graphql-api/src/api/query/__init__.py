from strawberry.tools import merge_types

from .helpers_query import HelpersQuery
from .pagination_query import PaginationQuery
from .search_query import SearchQuery
from .single_query import SingleQuery

Query = merge_types(
    "Query",
    (
        SingleQuery,
        PaginationQuery,
        SearchQuery,
        HelpersQuery,
    ),
)
