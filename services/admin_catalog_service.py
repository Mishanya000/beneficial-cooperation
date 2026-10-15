from sqlalchemy import select

from database.models import Category, Place
from database.session import SessionLocal


class AdminCatalogService:
    def get_categories(self) -> list[Category]:
        with SessionLocal() as session:
            statement = select(Category).order_by(Category.name)
            return list(session.scalars(statement).all())

    def get_places(self) -> list[Place]:
        with SessionLocal() as session:
            statement = select(Place).order_by(Place.name)
            return list(session.scalars(statement).all())

    def add_category(self, name: str) -> Category:
        name = name.strip()

        if not 1 <= len(name) <= 100:
            raise ValueError("Название должно содержать от 1 до 100 символов.")

        with SessionLocal.begin() as session:
            existing = session.scalar(
                select(Category).where(Category.name == name)
            )

            if existing is not None:
                raise ValueError("Такая категория уже существует.")

            category = Category(name=name)
            session.add(category)
            session.flush()

            category_id = category.id

        with SessionLocal() as session:
            return session.get(Category, category_id)

    def add_place(
        self,
        name: str,
        address: str,
        latitude: float,
        longitude: float,
    ) -> Place:
        name = name.strip()
        address = address.strip()

        if not 1 <= len(name) <= 150:
            raise ValueError("Название должно содержать от 1 до 150 символов.")

        if not 1 <= len(address) <= 300:
            raise ValueError("Адрес должен содержать от 1 до 300 символов.")

        if not -90 <= latitude <= 90:
            raise ValueError("Широта должна быть от -90 до 90.")

        if not -180 <= longitude <= 180:
            raise ValueError("Долгота должна быть от -180 до 180.")

        with SessionLocal.begin() as session:
            place = Place(
                name=name,
                address=address,
                latitude=latitude,
                longitude=longitude,
            )

            session.add(place)
            session.flush()

            place_id = place.id

        with SessionLocal() as session:
            return session.get(Place, place_id)