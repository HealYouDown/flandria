import os

ENGINE_ECHO = os.getenv("ENGINE_ECHO", "false").lower() == "true"
DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///database.sqlite3")
