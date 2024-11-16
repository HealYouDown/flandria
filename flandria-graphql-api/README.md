# Florensia GraphQL-API
This repository contains the GraphQL API Backend for Flandria. Also included is an updater and asset generation script, based on the live patch server files of Florensia.


## Development
You should have the following:
- Visual Studio Code (see profile in `.vscode`)
- Poetry installed
- Docker installed

### Environment Variables
You can set the following variables (in a `.env` file):
- `ENGINE_ECHO`: `false|true` - Echos SQLAlchemy Engine Commands
- `DATABASE_URI`: `DB URI for SQLAlchemy` - Database to connect to, see below.  

### Database setup
You can start a local Postgres database using `docker run --name flandria-db -p 5432:5432 -e POSTGRES_PASSWORD=123 -d postgres`.
To use postgres as a database, you need to set the `DATABASE_URI` environment variable to `postgresql+psycopg2://postgres:123@localhost:5432/postgres` (e.g. in a `.env` file).

If no env variable is found, the application defaults to a local sqlite database: `database.sqlite3`.

To populate the database with everything in one go: `python manage.py database init && python manage.py database update && python manage.py database drops maps stats models && python manage.py database prune`

### Run GraphQL API
To start the local GraphQL Debug server, run `python manage.py api debug` (which interally runs `uvicorn src.api.app:app --reload`).


## Commands
All commands are run via `manage.py`.
In the following section, all commands are explained briefly. Most often they have additional flags than can be shown with `--help`.

### API
The `api` group has the following commands:
- `codegen` - generates files for our GraphQL API based on the SQLAlchemy models.
- `debug` - starts the local debug server.
- `export-schema` - exports the schema to the given path, e.g. `[...] api export-schema ../flandria-frontend/schema.graphql`

### Assets
The `assets` group has the following commands:
- `icons`
  - `download` - downloads all required icons (a populated database is required) to `tmp/icons`.
  - `extract` - extracts the icons to the local `assets/icons` folder.
- `models`
  - `download` - downloads all monster, npc and item model files and textures to `tmp/models/(items|monster|npc)/...`.
  - `process` - processes the models using `noesis` and converts them to `gltf` JSON files. The `gltf` files are stored in `assets/models/(weapon|armor|dress|hat|monster|npc)`. See [3D Models](./docs/3d_Models.md) for more information.
  Using any combination of the folder names above as an argument to `process`, you can limit what models are converted.

### Database
The `database` group has the following commands:
- `download` - downloads the required files to update the database to `tmp/...`.
- `update` - Popuplates the database with the downloaded files.
- `drops` - loads the drop files from `tmp/drops/<code>.xml` into the database.
- `maps` - loads the map files (monster and npc positions) from `tmp/maps/<map_code>/...` into the database.
- `stats` - loads the player stats files from `data/stats/...` into the database.
- `init` - Drops the whole database and re-creates the schema. Note that all existing data will be lost.
- `prune` - Fixes all foreign key violations. Recommended to always run after data was loaded.
