from sqlalchemy import select
from sqlalchemy.orm import joinedload

from database.models import Discount, DiscountReport
from database.session import SessionLocal


class AdminReportService:
    def get_pending_reports(self) -> list[DiscountReport]:
        with SessionLocal() as session:
            statement = (
                select(DiscountReport)
                .options(joinedload(DiscountReport.discount))
                .where(DiscountReport.status == "pending")
                .order_by(DiscountReport.created_at.desc())
            )

            return list(session.scalars(statement).all())

    def get_report(self, report_id: int) -> DiscountReport | None:
        with SessionLocal() as session:
            statement = (
                select(DiscountReport)
                .options(joinedload(DiscountReport.discount))
                .where(DiscountReport.id == report_id)
            )

            return session.scalar(statement)

    def resolve_report(self, report_id: int) -> None:
        with SessionLocal.begin() as session:
            report = session.get(DiscountReport, report_id)

            if report is None:
                raise ValueError("Жалоба не найдена.")

            if report.status != "pending":
                raise ValueError("Жалоба уже обработана.")

            discount = session.get(Discount, report.discount_id)

            if discount is None:
                raise ValueError("Скидка не найдена.")

            discount.is_active = False
            report.status = "resolved"

    def reject_report(self, report_id: int) -> None:
        with SessionLocal.begin() as session:
            report = session.get(DiscountReport, report_id)

            if report is None:
                raise ValueError("Жалоба не найдена.")

            if report.status != "pending":
                raise ValueError("Жалоба уже обработана.")

            report.status = "rejected"