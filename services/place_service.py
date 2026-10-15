from database.models import Place
from database.session import SessionLocal
from repositories.place_repository import PlaceRepository


class PlaceService:
    def get_places_with_discounts(self) -> list[Place]:
        with SessionLocal() as session:
            repository = PlaceRepository(session)
            return repository.get_with_active_discounts()

    def get_place(self, place_id: int) -> Place | None:
        with SessionLocal() as session:
            repository = PlaceRepository(session)
            return repository.get_by_id(place_id)