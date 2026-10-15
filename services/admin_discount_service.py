from datetime import date

from sqlalchemy import select, func

from database.models import (
    Discount,
    Place,
    Category,
    User,
    Review,
    DiscountReport,
)
from database.session import SessionLocal


class AdminDiscountService:

    def add_discount(
        self,
        title: str,
        description: str,
        discount_percent: int | None,
        conditions: str,
        valid_until: date | None,
        place_id: int,
        category_id: int,
    ) -> Discount:
        title = title.strip()
        description = description.strip()
        conditions = conditions.strip()

        if not 1 <= len(title) <= 150:
            raise ValueError("Название должно содержать 1–150 символов.")

        if not 1 <= len(description) <= 2000:
            raise ValueError("Описание должно содержать 1–2000 символов.")

        if not 1 <= len(conditions) <= 1000:
            raise ValueError("Условия должны содержать 1–1000 символов.")

        if discount_percent is not None and not 0 <= discount_percent <= 100:
            raise ValueError("Процент должен быть от 0 до 100.")

        if valid_until is not None and valid_until < date.today():
            raise ValueError("Дата окончания не может быть в прошлом.")

        with SessionLocal.begin() as session:
            if session.get(Place, place_id) is None:
                raise ValueError("Заведение не найдено.")

            if session.get(Category, category_id) is None:
                raise ValueError("Категория не найдена.")

            discount = Discount(
                title=title,
                description=description,
                discount_percent=discount_percent,
                conditions=conditions,
                valid_until=valid_until,
                place_id=place_id,
                category_id=category_id,
                is_active=True,
            )

            session.add(discount)
            session.flush()

            discount_id = discount.id

        with SessionLocal() as session:
            return session.get(Discount, discount_id)

    def get_all_discounts(self) -> list[Discount]:
        with SessionLocal() as session:
            statement = select(Discount).order_by(Discount.id.desc())
            return list(session.scalars(statement).all())

    def toggle_discount(self, discount_id: int) -> bool:
        with SessionLocal.begin() as session:
            discount = session.get(Discount, discount_id)

            if discount is None:
                raise ValueError("Скидка не найдена.")

            discount.is_active = not discount.is_active
            return discount.is_active

    def get_statistics(self) -> dict[str, int]:
        with SessionLocal() as session:
            return {
                "users": session.scalar(select(func.count(User.id))) or 0,
                "places": session.scalar(select(func.count(Place.id))) or 0,
                "categories": session.scalar(select(func.count(Category.id))) or 0,
                "discounts": session.scalar(select(func.count(Discount.id))) or 0,
                "active_discounts": session.scalar(
                    select(func.count(Discount.id)).where(
                        Discount.is_active.is_(True),
                        (Discount.valid_until.is_(None))
                        | (Discount.valid_until >= date.today()),
                    )
                ) or 0,
                "reviews": session.scalar(select(func.count(Review.id))) or 0,
                "reports": session.scalar(
                    select(func.count(DiscountReport.id))
                ) or 0,
                "pending_reports": session.scalar(
                    select(func.count(DiscountReport.id)).where(
                        DiscountReport.status == "pending"
                    )
                ) or 0,
            }