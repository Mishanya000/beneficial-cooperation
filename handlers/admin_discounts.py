from telebot import TeleBot
from telebot.types import CallbackQuery

from keyboards.admin import (
    create_admin_keyboard,
    create_admin_discounts_keyboard,
    create_admin_place_selection,
    create_admin_category_selection,
)
from services.admin_service import AdminService
from services.admin_catalog_service import AdminCatalogService
from services.admin_discount_service import AdminDiscountService
from services.dialog_state import dialog_state


def register_admin_discount_handlers(bot: TeleBot) -> None:
    admin_service = AdminService()
    catalog_service = AdminCatalogService()
    discount_service = AdminDiscountService()

    def check_admin(call: CallbackQuery) -> bool:
        if not admin_service.is_admin(call.from_user.id):
            bot.answer_callback_query(
                call.id,
                "⛔ Доступ запрещён.",
                show_alert=True,
            )
            return False

        bot.answer_callback_query(call.id)
        return True

    @bot.callback_query_handler(
        func=lambda call: call.data == "admin:add_discount"
    )
    def start_add_discount(call: CallbackQuery) -> None:
        if not check_admin(call):
            return

        dialog_state.set(
            call.message.chat.id,
            call.from_user.id,
            {
                "action": "admin_add_discount",
                "step": "title",
                "data": {},
            },
        )

        bot.send_message(
            call.message.chat.id,
            "🔥 Введи название скидки.\n\n"
            "Для отмены отправь /cancel",
        )

    @bot.callback_query_handler(
        func=lambda call: call.data == "admin:discounts"
    )
    def show_discounts(call: CallbackQuery) -> None:
        if not check_admin(call):
            return

        discounts = discount_service.get_all_discounts()

        if not discounts:
            bot.send_message(
                call.message.chat.id,
                "Пока скидок нет.",
                reply_markup=create_admin_keyboard(),
            )
            return

        bot.send_message(
            call.message.chat.id,
            "🔥 Управление скидками\n\n"
            "Нажми на скидку, чтобы включить или отключить её.",
            reply_markup=create_admin_discounts_keyboard(discounts),
        )

    @bot.callback_query_handler(
        func=lambda call: call.data.startswith("admin:discount:toggle:")
    )
    def toggle_discount(call: CallbackQuery) -> None:
        if not check_admin(call):
            return

        discount_id = int(call.data.split(":")[-1])

        try:
            is_active = discount_service.toggle_discount(discount_id)
        except ValueError as error:
            bot.send_message(call.message.chat.id, f"❌ {error}")
            return

        status = "включена 🟢" if is_active else "отключена 🔴"

        bot.send_message(
            call.message.chat.id,
            f"✅ Скидка {status}.",
            reply_markup=create_admin_discounts_keyboard(
                discount_service.get_all_discounts()
            ),
        )

    @bot.callback_query_handler(
        func=lambda call: call.data.startswith("admin:select_place:")
    )
    def select_place(call: CallbackQuery) -> None:
        if not check_admin(call):
            return

        state = dialog_state.get(
            call.message.chat.id,
            call.from_user.id,
        )

        if state is None or state.get("action") != "admin_add_discount":
            bot.send_message(call.message.chat.id, "❌ Диалог устарел.")
            return

        if state.get("step") != "place":
            bot.send_message(call.message.chat.id, "❌ Сейчас не выбирается заведение.")
            return

        place_id = int(call.data.split(":")[-1])

        places = catalog_service.get_places()
        if not any(place.id == place_id for place in places):
            bot.send_message(call.message.chat.id, "❌ Заведение не найдено.")
            return

        data = state["data"].copy()
        data["place_id"] = place_id

        dialog_state.set(
            call.message.chat.id,
            call.from_user.id,
            {
                "action": "admin_add_discount",
                "step": "category",
                "data": data,
            },
        )

        bot.send_message(
            call.message.chat.id,
            "📂 Теперь выбери категорию:",
            reply_markup=create_admin_category_selection(
                catalog_service.get_categories()
            ),
        )

    @bot.callback_query_handler(
        func=lambda call: call.data.startswith("admin:select_category:")
    )
    def select_category(call: CallbackQuery) -> None:
        if not check_admin(call):
            return

        state = dialog_state.get(
            call.message.chat.id,
            call.from_user.id,
        )

        if state is None or state.get("action") != "admin_add_discount":
            bot.send_message(call.message.chat.id, "❌ Диалог устарел.")
            return

        if state.get("step") != "category":
            bot.send_message(call.message.chat.id, "❌ Сейчас не выбирается категория.")
            return

        category_id = int(call.data.split(":")[-1])

        categories = catalog_service.get_categories()
        if not any(category.id == category_id for category in categories):
            bot.send_message(call.message.chat.id, "❌ Категория не найдена.")
            return

        data = state["data"]

        try:
            discount = discount_service.add_discount(
                title=data["title"],
                description=data["description"],
                discount_percent=data["discount_percent"],
                conditions=data["conditions"],
                valid_until=data["valid_until"],
                place_id=data["place_id"],
                category_id=category_id,
            )
        except ValueError as error:
            bot.send_message(call.message.chat.id, f"❌ {error}")
            return

        dialog_state.clear(call.message.chat.id, call.from_user.id)

        bot.send_message(
            call.message.chat.id,
            f"✅ Скидка «{discount.title}» успешно добавлена!",
            reply_markup=create_admin_keyboard(),
        )

    @bot.callback_query_handler(
        func=lambda call: call.data == "admin:stats"
    )
    def show_stats(call: CallbackQuery) -> None:
        if not check_admin(call):
            return

        stats = discount_service.get_statistics()

        text = (
            "📊 Статистика бота\n\n"
            f"👥 Пользователи: {stats['users']}\n"
            f"🏪 Заведения: {stats['places']}\n"
            f"📂 Категории: {stats['categories']}\n"
            f"🔥 Всего скидок: {stats['discounts']}\n"
            f"🟢 Действующие скидки: {stats['active_discounts']}\n"
            f"⭐ Отзывы: {stats['reviews']}\n"
            f"🚩 Жалобы: {stats['reports']}\n"
            f"⏳ Ожидают рассмотрения: {stats['pending_reports']}"
        )

        bot.send_message(
            call.message.chat.id,
            text,
            reply_markup=create_admin_keyboard(),
        )