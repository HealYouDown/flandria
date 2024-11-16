import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.core.enums import MonsterMessageTrigger
from src.database.base import Base
from src.updater import strategies
from src.updater.schema import LoaderInfo


class ActorMessage(Base):
    loader_info = LoaderInfo(
        files=LoaderInfo.Files(
            client_files=["c_ObjChat.bin"],
            string_files=["ObjChatDesc.dat"],
        ),
        loader_strategy=strategies.actor_message,
    )

    index = orm.mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
    )
    code = orm.mapped_column(
        sa.String(32),
        doc="Message object code",
        index=True,
    )
    trigger = orm.mapped_column(
        sa.Enum(MonsterMessageTrigger),
        nullable=False,
        doc="Message trigger (e.g. on die, on attack, ...)",
    )
    message = orm.mapped_column(
        sa.Text,
        nullable=False,
        doc="Message content",
    )
