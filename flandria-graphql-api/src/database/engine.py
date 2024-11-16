import sqlalchemy.orm as orm
from sqlalchemy import create_engine

from src.config import DATABASE_URI, ENGINE_ECHO

engine = create_engine(DATABASE_URI, echo=ENGINE_ECHO)
Session = orm.sessionmaker(engine)
