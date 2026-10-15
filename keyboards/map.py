from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from database.models import Place


def create_places_keyboard(
    places: list[Place],
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)

    for place in places:
        keyboard.add(
            InlineKeyboardButton(
                text=f"📍 {place.name}",
                callback_data=f"place:{place.id}",
            )
        )

    keyboard.add(
        InlineKeyboardButton(
            text="⬅️ Главное меню",
            callback_data="main_menu",
        )
    )

    return keyboard