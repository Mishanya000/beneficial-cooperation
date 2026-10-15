from database.models import Category
from database.session import SessionLocal
from repositories.category_repository import CategoryRepository


class CategoryService:
    def get_categories(self) -> list[Category]:
        with SessionLocal() as session:
            repository = CategoryRepository(session)
            return repository.get_all()