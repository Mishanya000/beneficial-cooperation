from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.models import Discount


def create_reviews_keyboard(discount_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(
        InlineKeyboardButton(
            "✍️ Оставить отзыв",
            callback_data=f"review:add:{discount_id}",
        ),
        InlineKeyboardButton(
            "🚩 Пожаловаться",
            callback_data=f"report:add:{discount_id}",
        ),
        InlineKeyboardButton(
            "⬅️ К скидке",
            callback_data=f"discount:{discount_id}",
        ),
    )

    return keyboard


def create_rating_keyboard(discount_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=5)

    buttons = [
        InlineKeyboardButton(
            f"{rating} ⭐",
            callback_data=f"review:rating:{discount_id}:{rating}",
        )
        for rating in range(1, 6)
    ]

    keyboard.add(*buttons)

    return keyboard


def create_reviews_list_keyboard(
        discounts: list[Discount],
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)

    for discount in discounts:
        keyboard.add(
            InlineKeyboardButton(
                text=f"⭐ {discount.title}",
                callback_data=f"reviews:{discount.id}",
            )
        )

    keyboard.add(
        InlineKeyboardButton(
            text="⬅️ Главное меню",
            callback_data="main_menu",
        )
    )

    return keyboard
