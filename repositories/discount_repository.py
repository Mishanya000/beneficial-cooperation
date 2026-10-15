from datetime import date

from sqlalchemy import or_, select
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from database.models import Place

from database.models import Discount


class DiscountRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_active(self) -> list[Discount]:
        statement = (
            select(Discount)
            .options(
                joinedload(Discount.place),
                joinedload(Discount.category),
            )
            .where(
                Discount.is_active.is_(True),
                or_(
                    Discount.valid_until.is_(None),
                    Discount.valid_until >= date.today(),
                ),
            )
            .order_by(Discount.id)
        )

        return list(self._session.scalars(statement).all())

    def get_by_id(self, discount_id: int) -> Discount | None:
        statement = (
            select(Discount)
            .options(
                joinedload(Discount.place),
                joinedload(Discount.category),
            )
            .where(Discount.id == discount_id)
        )

        return self._session.scalar(statement)

    def add(self, discount: Discount) -> None:
        self._session.add(discount)
        self._session.flush()

    def search_by_name(self, query: str) -> list[Discount]:
        statement = (
            select(Discount)
            .join(Discount.place)
            .options(
                joinedload(Discount.place),
                joinedload(Discount.category),
            )
            .where(
                Discount.is_active.is_(True),
                or_(
                    Discount.valid_until.is_(None),
                    Discount.valid_until >= date.today(),
                ),
                or_(
                    func.lower(Discount.title).contains(query.lower()),
                    func.lower(Place.name).contains(query.lower()),
                ),
            )
            .order_by(Discount.id)
        )

        return list(self._session.scalars(statement).all())

    def get_by_min_percent(self, percent: int) -> list[Discount]:
        statement = (
            select(Discount)
            .options(
                joinedload(Discount.place),
                joinedload(Discount.category),
            )
            .where(
                Discount.is_active.is_(True),
                or_(
                    Discount.valid_until.is_(None),
                    Discount.valid_until >= date.today(),
                ),
                Discount.discount_percent >= percent,
            )
            .order_by(Discount.discount_percent.desc())
        )

        return list(self._session.scalars(statement).all())

    def get_by_category(self, category_id: int) -> list[Discount]:
        statement = (
            select(Discount)
            .options(
                joinedload(Discount.place),
                joinedload(Discount.category),
            )
            .where(
                Discount.is_active.is_(True),
                or_(
                    Discount.valid_until.is_(None),
                    Discount.valid_until >= date.today(),
                ),
                Discount.category_id == category_id,
            )
            .order_by(Discount.id)
        )

        return list(self._session.scalars(statement).all())