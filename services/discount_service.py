from datetime import date

from database.models import Discount
from database.session import SessionLocal
from repositories.discount_repository import DiscountRepository


class DiscountService:
    def get_active_discounts(self) -> list[Discount]:
        with SessionLocal() as session:
            repository = DiscountRepository(session)
            return repository.get_active()

    def get_discount(self, discount_id: int) -> Discount | None:
        with SessionLocal() as session:
            repository = DiscountRepository(session)

            discount = repository.get_by_id(discount_id)

            if discount is None:
                return None

            if not discount.is_active:
                return None

            if (
                discount.valid_until is not None
                and discount.valid_until < date.today()
            ):
                return None

            return discount

    def search_discounts(self, query: str) -> list[Discount]:
        with SessionLocal() as session:
            repository = DiscountRepository(session)
            return repository.search_by_name(query.strip())

    def get_discounts_by_percent(self, percent: int) -> list[Discount]:
        if not 0 <= percent <= 100:
            raise ValueError("Percent must be between 0 and 100")

        with SessionLocal() as session:
            repository = DiscountRepository(session)
            return repository.get_by_min_percent(percent)

    def get_discounts_by_category(
            self,
            category_id: int,
    ) -> list[Discount]:
        with SessionLocal() as session:
            repository = DiscountRepository(session)
            return repository.get_by_category(category_id)