from sqlalchemy import func, select
from sqlalchemy.orm import Session

from database.models import Review


class ReviewRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_by_discount(self, discount_id: int) -> list[Review]:
        statement = (
            select(Review)
            .where(Review.discount_id == discount_id)
            .order_by(Review.created_at.desc())
            .limit(10)
        )

        return list(self._session.scalars(statement).all())

    def get_average_rating(self, discount_id: int) -> float | None:
        statement = select(
            func.avg(Review.rating)
        ).where(
            Review.discount_id == discount_id
        )

        result = self._session.scalar(statement)

        return float(result) if result is not None else None

    def add(self, review: Review) -> None:
        self._session.add(review)
        self._session.flush()