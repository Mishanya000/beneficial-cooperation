from datetime import date, timedelta

from sqlalchemy import select

from database.models import Category, Discount, Place
from database.session import SessionLocal


CATEGORIES = [
    "Еда и напитки",
    "Развлечения",
    "Учёба",
    "Здоровье",
]


def seed_database() -> None:
    with SessionLocal.begin() as session:
        existing_categories = {
            category.name: category
            for category in session.scalars(select(Category)).all()
        }

        for name in CATEGORIES:
            if name not in existing_categories:
                category = Category(name=name)
                session.add(category)
                existing_categories[name] = category

        existing_demo = session.scalar(
            select(Discount.id).where(
                Discount.title == "Демо: скидка на кофе"
            )
        )

        if existing_demo is not None:
            return

        place = Place(
            name="Демо-кофейня",
            address="Санкт-Петербург, Невский проспект",
            latitude=59.9343,
            longitude=30.3351,
        )

        session.add(place)
        session.flush()

        discount = Discount(
            title="Демо: скидка на кофе",
            description="Тестовое предложение для проверки бота.",
            discount_percent=15,
            conditions="Предъявить студенческий билет.",
            valid_until=date.today() + timedelta(days=30),
            is_active=True,
            place_id=place.id,
            category_id=existing_categories["Еда и напитки"].id,
        )

        session.add(discount)