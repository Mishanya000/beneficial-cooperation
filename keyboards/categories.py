from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from database.models import Category


CATEGORY_EMOJIS = {
    "Еда и напитки": "🍔",
    "Развлечения": "🎮",
    "Учёба": "📚",
    "Здоровье": "💊",
}


def create_categories_keyboard(
    categories: list[Category],
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)

    buttons = []

    for category in categories:
        emoji = CATEGORY_EMOJIS.get(category.name, "📂")

        buttons.append(
            InlineKeyboardButton(
                text=f"{emoji} {category.name}",
                callback_data=f"category:{category.id}",
            )
        )

    keyboard.add(*buttons)

    keyboard.add(
        InlineKeyboardButton(
            text="⬅️ Главное меню",
            callback_data="main_menu",
        )
    )

    return keyboard