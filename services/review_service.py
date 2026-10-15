from database.models import Review, DiscountReport
from database.session import SessionLocal

from repositories.user_repository import UserRepository
from repositories.review_repository import ReviewRepository
from repositories.report_repository import ReportRepository
from repositories.discount_repository import DiscountRepository


class ReviewService:
    def get_reviews(self, discount_id: int):
        with SessionLocal() as session:
            repository = ReviewRepository(session)

            reviews = repository.get_by_discount(discount_id)
            average = repository.get_average_rating(discount_id)

            return reviews, average

    def add_review(
        self,
        telegram_id: int,
        username: str | None,
        discount_id: int,
        rating: int,
        comment: str,
    ) -> None:
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")

        if len(comment.strip()) > 1000:
            raise ValueError("Comment is too long")

        with SessionLocal.begin() as session:
            user_repository = UserRepository(session)
            discount_repository = DiscountRepository(session)
            review_repository = ReviewRepository(session)

            discount = discount_repository.get_by_id(discount_id)

            if discount is None or not discount.is_active:
                raise ValueError("Discount not found")

            user = user_repository.get_or_create(
                telegram_id,
                username,
            )

            review = Review(
                user_id=user.id,
                discount_id=discount_id,
                rating=rating,
                comment=comment.strip() or None,
            )

            review_repository.add(review)

    def add_report(
        self,
        telegram_id: int,
        username: str | None,
        discount_id: int,
        reason: str,
    ) -> None:
        reason = reason.strip()

        if not reason or len(reason) > 1000:
            raise ValueError("Reason must contain 1-1000 characters")

        with SessionLocal.begin() as session:
            user_repository = UserRepository(session)
            discount_repository = DiscountRepository(session)
            report_repository = ReportRepository(session)

            discount = discount_repository.get_by_id(discount_id)

            if discount is None or not discount.is_active:
                raise ValueError("Discount not found")

            user = user_repository.get_or_create(
                telegram_id,
                username,
            )

            report = DiscountReport(
                user_id=user.id,
                discount_id=discount_id,
                reason=reason,
                status="pending",
            )

            report_repository.add(report)