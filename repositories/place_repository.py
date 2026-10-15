from sqlalchemy import select
from sqlalchemy.orm import Session

from datetime import date

from sqlalchemy import or_

from database.models import Discount

from database.models import Place


class PlaceRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_all(self) -> list[Place]:
        statement = select(Place).order_by(Place.name)

        return list(self._session.scalars(statement).all())

    def get_by_id(self, place_id: int) -> Place | None:
        return self._session.get(Place, place_id)

    def add(self, place: Place) -> None:
        self._session.add(place)
        self._session.flush()

    def get_with_active_discounts(self) -> list[Place]:
        statement = (
            select(Place)
            .join(Place.discounts)
            .where(
                Discount.is_active.is_(True),
                or_(
                    Discount.valid_until.is_(None),
                    Discount.valid_until >= date.today(),
                ),
            )
            .distinct()
            .order_by(Place.name)
        )

        return list(self._session.scalars(statement).all())