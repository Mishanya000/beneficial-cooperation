from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_admin_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(
        InlineKeyboardButton(
            "➕ Добавить скидку",
            callback_data="admin:add_discount",
        ),
        InlineKeyboardButton(
            "🏪 Управление заведениями",
            callback_data="admin:places",
        ),
        InlineKeyboardButton(
            "📂 Управление категориями",
            callback_data="admin:categories",
        ),
        InlineKeyboardButton(
            "🔥 Управление скидками",
            callback_data="admin:discounts",
        ),
        InlineKeyboardButton(
            "🚩 Жалобы пользователей",
            callback_data="admin:reports",
        ),
        InlineKeyboardButton(
            "📊 Статистика",
            callback_data="admin:stats",
        ),
        InlineKeyboardButton(
            "⬅️ Главное меню",
            callback_data="main_menu",
        ),
    )

    return keyboard

def create_admin_places_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(
        InlineKeyboardButton(
            "➕ Добавить заведение",
            callback_data="admin:place:add",
        ),
        InlineKeyboardButton(
            "📋 Список заведений",
            callback_data="admin:place:list",
        ),
        InlineKeyboardButton(
            "⬅️ Админ-панель",
            callback_data="admin:menu",
        ),
    )

    return keyboard


def create_admin_categories_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(
        InlineKeyboardButton(
            "➕ Добавить категорию",
            callback_data="admin:category:add",
        ),
        InlineKeyboardButton(
            "📋 Список категорий",
            callback_data="admin:category:list",
        ),
        InlineKeyboardButton(
            "⬅️ Админ-панель",
            callback_data="admin:menu",
        ),
    )

    return keyboard