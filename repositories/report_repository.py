from sqlalchemy.orm import Session

from database.models import DiscountReport


class ReportRepository:
    def __init__(self, session: Session):
        self._session = session

    def add(self, report: DiscountReport) -> None:
        self._session.add(report)
        self._session.flush()