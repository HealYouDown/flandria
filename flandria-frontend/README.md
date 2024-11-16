# Flandria Frontend

Frontend for Flandria, built using Vite + React and shadecn.

## Deployment

To build the docker container, run `docker build --build-arg API_URL=<url> -t flandria .` where `API_URL` is the endpoint for our Backend (including the `/graphql` part). If no build arg is specified, `http://localhost:8000/graphql` is used.

E.g. `docker build --build-arg API_URL=https://flandria.wiki/api/graphql . -t flandria`

Assets (icons and models) are not built and have to be mounted to the container in `/usr/share/nginx/html/assets`.

## Dev notes

- Due to a bug in `graphql-lsp`, fragments are currently marked as `unknown`, until the file with its definition is saved manually. See issue [3066](https://github.com/graphql/graphiql/issues/3066).
