from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from database.models import Discount


def create_discounts_keyboard(
    discounts: list[Discount],
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)

    for discount in discounts:
        label = discount.title

        if discount.discount_percent is not None:
            label += f" — {discount.discount_percent}%"

        keyboard.add(
            InlineKeyboardButton(
                text=label,
                callback_data=f"discount:{discount.id}",
            )
        )

    keyboard.add(
        InlineKeyboardButton(
            text="⬅️ Главное меню",
            callback_data="main_menu",
        )
    )

    return keyboard


def create_discount_details_keyboard(
    discount_id: int,
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(
        InlineKeyboardButton(
            text="🗺 Показать на карте",
            callback_data=f"location:{discount_id}",
        ),
        InlineKeyboardButton(
            text="⭐ Отзывы",
            callback_data=f"reviews:{discount_id}",
        ),
        InlineKeyboardButton(
            text="⬅️ К списку скидок",
            callback_data="discounts",
        ),
    )

    return keyboard