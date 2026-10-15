from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import Category


class CategoryRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_all(self) -> list[Category]:
        statement = select(Category).order_by(Category.name)

        return list(self._session.scalars(statement).all())

    def get_by_id(self, category_id: int) -> Category | None:
        return self._session.get(Category, category_id)

    def add(self, category: Category) -> None:
        self._session.add(category)
        self._session.flush()