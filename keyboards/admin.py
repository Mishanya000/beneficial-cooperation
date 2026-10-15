from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.models import Discount, Place, Category
from database.models import DiscountReport


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


def create_admin_discounts_keyboard(
        discounts: list[Discount],
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)

    for discount in discounts[:30]:
        status = "🟢" if discount.is_active else "🔴"

        keyboard.add(
            InlineKeyboardButton(
                f"{status} {discount.title}",
                callback_data=f"admin:discount:toggle:{discount.id}",
            )
        )

    keyboard.add(
        InlineKeyboardButton(
            "⬅️ Админ-панель",
            callback_data="admin:menu",
        )
    )

    return keyboard


def create_admin_place_selection(
        places: list[Place],
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)

    for place in places:
        keyboard.add(
            InlineKeyboardButton(
                place.name,
                callback_data=f"admin:select_place:{place.id}",
            )
        )

    keyboard.add(
        InlineKeyboardButton(
            "❌ Отмена",
            callback_data="admin:menu",
        )
    )

    return keyboard


def create_admin_category_selection(
        categories: list[Category],
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)

    for category in categories:
        keyboard.add(
            InlineKeyboardButton(
                category.name,
                callback_data=f"admin:select_category:{category.id}",
            )
        )

    keyboard.add(
        InlineKeyboardButton(
            "❌ Отмена",
            callback_data="admin:menu",
        )
    )

    return keyboard

def create_admin_reports_keyboard(
    reports: list[DiscountReport],
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)

    for report in reports[:30]:
        keyboard.add(
            InlineKeyboardButton(
                text=f"🚩 Жалоба #{report.id}",
                callback_data=f"admin:report:view:{report.id}",
            )
        )

    keyboard.add(
        InlineKeyboardButton(
            "⬅️ Админ-панель",
            callback_data="admin:menu",
        )
    )

    return keyboard


def create_admin_report_actions_keyboard(
    report_id: int,
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(
        InlineKeyboardButton(
            "✅ Принять и отключить скидку",
            callback_data=f"admin:report:resolve:{report_id}",
        ),
        InlineKeyboardButton(
            "❌ Отклонить жалобу",
            callback_data=f"admin:report:reject:{report_id}",
        ),
        InlineKeyboardButton(
            "⬅️ К жалобам",
            callback_data="admin:reports",
        ),
    )

    return keyboard