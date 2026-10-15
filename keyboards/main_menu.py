from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_main_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)

    keyboard.add(
        InlineKeyboardButton("🔥 Скидки", callback_data="discounts"),
        InlineKeyboardButton("🗺 Карта", callback_data="map"),
    )

    keyboard.add(
        InlineKeyboardButton("🔎 Поиск", callback_data="search"),
        InlineKeyboardButton("📂 Категории", callback_data="categories"),
    )

    keyboard.add(
        InlineKeyboardButton("⭐ Отзывы", callback_data="reviews"),
        InlineKeyboardButton("ℹ️ Помощь", callback_data="help"),
    )

    return keyboard