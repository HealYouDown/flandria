from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from strawberry.asgi import GraphQL

from .schema import schema

graphql_app = GraphQL(schema)

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origin_regex=r"https?:\/\/localhost(:\d+)?",
        allow_methods=["GET", "POST"],
    )
]

app = Starlette(middleware=middleware)
app.add_route("/graphql", graphql_app)  # type: ignore
app.add_websocket_route("/graphql", graphql_app)  # type: ignore
