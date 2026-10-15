from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_search_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(
        InlineKeyboardButton(
            text="🏪 По названию",
            callback_data="search:name",
        ),
        InlineKeyboardButton(
            text="💰 По размеру скидки",
            callback_data="search:percent",
        ),
        InlineKeyboardButton(
            text="⬅️ Главное меню",
            callback_data="main_menu",
        ),
    )

    return keyboard