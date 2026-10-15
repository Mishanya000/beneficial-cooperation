from telebot import TeleBot
from telebot.types import CallbackQuery, Message

from keyboards.admin import (
    create_admin_keyboard,
    create_admin_places_keyboard,
    create_admin_categories_keyboard,
)
from services.admin_service import AdminService
from services.admin_catalog_service import AdminCatalogService
from services.dialog_state import dialog_state


def register_admin_handlers(bot: TeleBot) -> None:
    admin_service = AdminService()
    catalog_service = AdminCatalogService()

    def is_allowed(user_id: int) -> bool:
        return admin_service.is_admin(user_id)

    @bot.message_handler(commands=["admin"])
    def open_admin_panel(message: Message) -> None:
        if not is_allowed(message.from_user.id):
            bot.send_message(
                message.chat.id,
                "⛔ У тебя нет доступа к админ-панели.",
            )
            return

        dialog_state.clear(message.chat.id, message.from_user.id)

        bot.send_message(
            message.chat.id,
            "🛠 Панель администратора\n\nВыбери действие:",
            reply_markup=create_admin_keyboard(),
        )

    @bot.callback_query_handler(
        func=lambda call: call.data == "admin:menu"
    )
    def show_admin_menu(call: CallbackQuery) -> None:
        if not is_allowed(call.from_user.id):
            bot.answer_callback_query(
                call.id, "⛔ Доступ запрещён.", show_alert=True
            )
            return

        bot.answer_callback_query(call.id)
        dialog_state.clear(call.message.chat.id, call.from_user.id)

        bot.send_message(
            call.message.chat.id,
            "🛠 Панель администратора:",
            reply_markup=create_admin_keyboard(),
        )

    @bot.callback_query_handler(
        func=lambda call: call.data == "admin:places"
    )
    def show_places_menu(call: CallbackQuery) -> None:
        if not is_allowed(call.from_user.id):
            bot.answer_callback_query(
                call.id, "⛔ Доступ запрещён.", show_alert=True
            )
            return

        bot.answer_callback_query(call.id)

        bot.send_message(
            call.message.chat.id,
            "🏪 Управление заведениями:",
            reply_markup=create_admin_places_keyboard(),
        )

    @bot.callback_query_handler(
        func=lambda call: call.data == "admin:categories"
    )
    def show_categories_menu(call: CallbackQuery) -> None:
        if not is_allowed(call.from_user.id):
            bot.answer_callback_query(
                call.id, "⛔ Доступ запрещён.", show_alert=True
            )
            return

        bot.answer_callback_query(call.id)

        bot.send_message(
            call.message.chat.id,
            "📂 Управление категориями:",
            reply_markup=create_admin_categories_keyboard(),
        )

    @bot.callback_query_handler(
        func=lambda call: call.data == "admin:category:list"
    )
    def list_categories(call: CallbackQuery) -> None:
        if not is_allowed(call.from_user.id):
            bot.answer_callback_query(
                call.id, "⛔ Доступ запрещён.", show_alert=True
            )
            return

        bot.answer_callback_query(call.id)

        categories = catalog_service.get_categories()

        text = "📂 Категории:\n\n"

        for category in categories:
            text += f"• {category.id}. {category.name}\n"

        if not categories:
            text += "Пока категорий нет."

        bot.send_message(
            call.message.chat.id,
            text,
            reply_markup=create_admin_categories_keyboard(),
        )

    @bot.callback_query_handler(
        func=lambda call: call.data == "admin:place:list"
    )
    def list_places(call: CallbackQuery) -> None:
        if not is_allowed(call.from_user.id):
            bot.answer_callback_query(
                call.id, "⛔ Доступ запрещён.", show_alert=True
            )
            return

        bot.answer_callback_query(call.id)

        places = catalog_service.get_places()

        if not places:
            text = "🏪 Пока заведений нет."
        else:
            lines = ["🏪 Список заведений:\n"]

            for place in places:
                lines.append(
                    f"{place.id}. {place.name}\n"
                    f"📍 {place.address}"
                )

            text = "\n\n".join(lines)

        bot.send_message(
            call.message.chat.id,
            text[:4000],
            reply_markup=create_admin_places_keyboard(),
        )

    @bot.callback_query_handler(
        func=lambda call: call.data == "admin:category:add"
    )
    def start_add_category(call: CallbackQuery) -> None:
        if not is_allowed(call.from_user.id):
            bot.answer_callback_query(
                call.id, "⛔ Доступ запрещён.", show_alert=True
            )
            return

        bot.answer_callback_query(call.id)

        dialog_state.set(
            call.message.chat.id,
            call.from_user.id,
            {
                "action": "admin_add_category",
            },
        )

        bot.send_message(
            call.message.chat.id,
            "📂 Введи название новой категории.\n\n"
            "Для отмены отправь /cancel",
        )

    @bot.callback_query_handler(
        func=lambda call: call.data == "admin:place:add"
    )
    def start_add_place(call: CallbackQuery) -> None:
        if not is_allowed(call.from_user.id):
            bot.answer_callback_query(
                call.id, "⛔ Доступ запрещён.", show_alert=True
            )
            return

        bot.answer_callback_query(call.id)

        dialog_state.set(
            call.message.chat.id,
            call.from_user.id,
            {
                "action": "admin_add_place",
                "step": "name",
                "data": {},
            },
        )

        bot.send_message(
            call.message.chat.id,
            "🏪 Введи название заведения.\n\n"
            "Для отмены отправь /cancel",
        )

    @bot.callback_query_handler(
        func=lambda call: call.data.startswith("admin:")
    )
    def other_admin_sections(call: CallbackQuery) -> None:
        if not is_allowed(call.from_user.id):
            bot.answer_callback_query(
                call.id, "⛔ Доступ запрещён.", show_alert=True
            )
            return

        bot.answer_callback_query(call.id)

        bot.send_message(
            call.message.chat.id,
            "🚧 Этот раздел пока в разработке.",
            reply_markup=create_admin_keyboard(),
        )