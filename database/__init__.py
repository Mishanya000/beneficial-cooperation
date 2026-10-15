from database.base import Base
from database.session import engine

import database.models  # noqa: F401


def init_db() -> None:
    Base.metadata.create_all(bind=engine)