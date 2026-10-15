from datetime import date, datetime, timezone

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(
        BigInteger, unique=True, nullable=False
    )
    username: Mapped[str | None] = mapped_column(String(100))
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now
    )

    reviews: Mapped[list["Review"]] = relationship(
        back_populates="user"
    )
    reports: Mapped[list["DiscountReport"]] = relationship(
        back_populates="user"
    )


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False
    )

    discounts: Mapped[list["Discount"]] = relationship(
        back_populates="category"
    )


class Place(Base):
    __tablename__ = "places"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    address: Mapped[str] = mapped_column(String(300))

    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)

    discounts: Mapped[list["Discount"]] = relationship(
        back_populates="place"
    )

    __table_args__ = (
        CheckConstraint(
            "latitude BETWEEN -90 AND 90",
            name="valid_latitude",
        ),
        CheckConstraint(
            "longitude BETWEEN -180 AND 180",
            name="valid_longitude",
        ),
    )


class Discount(Base):
    __tablename__ = "discounts"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)

    discount_percent: Mapped[int | None] = mapped_column(Integer)
    conditions: Mapped[str] = mapped_column(Text)

    valid_until: Mapped[date | None] = mapped_column(Date)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    place_id: Mapped[int] = mapped_column(
        ForeignKey("places.id")
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id")
    )

    place: Mapped["Place"] = relationship(
        back_populates="discounts"
    )
    category: Mapped["Category"] = relationship(
        back_populates="discounts"
    )

    reviews: Mapped[list["Review"]] = relationship(
        back_populates="discount"
    )
    reports: Mapped[list["DiscountReport"]] = relationship(
        back_populates="discount"
    )

    __table_args__ = (
        CheckConstraint(
            "discount_percent BETWEEN 0 AND 100",
            name="valid_discount_percent",
        ),
    )


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )
    discount_id: Mapped[int] = mapped_column(
        ForeignKey("discounts.id")
    )

    rating: Mapped[int] = mapped_column(Integer)
    comment: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now
    )

    user: Mapped["User"] = relationship(
        back_populates="reviews"
    )
    discount: Mapped["Discount"] = relationship(
        back_populates="reviews"
    )

    __table_args__ = (
        CheckConstraint(
            "rating BETWEEN 1 AND 5",
            name="valid_review_rating",
        ),
    )


class DiscountReport(Base):
    __tablename__ = "discount_reports"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )
    discount_id: Mapped[int] = mapped_column(
        ForeignKey("discounts.id")
    )

    reason: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(
        String(20), default="pending"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now
    )

    user: Mapped["User"] = relationship(
        back_populates="reports"
    )
    discount: Mapped["Discount"] = relationship(
        back_populates="reports"
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'resolved', 'rejected')",
            name="valid_report_status",
        ),
    )