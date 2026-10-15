from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import User


class UserRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_by_telegram_id(self, telegram_id: int) -> User | None:
        statement = select(User).where(
            User.telegram_id == telegram_id
        )
        return self._session.scalar(statement)

    def get_or_create(
        self,
        telegram_id: int,
        username: str | None,
    ) -> User:
        user = self.get_by_telegram_id(telegram_id)

        if user is not None:
            return user

        user = User(
            telegram_id=telegram_id,
            username=username,
        )

        self._session.add(user)
        self._session.flush()

        return user