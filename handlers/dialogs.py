from telebot import TeleBot
from telebot.types import Message

from keyboards.discounts import create_discounts_keyboard
from keyboards.reviews import create_reviews_keyboard
from keyboards.search import create_search_keyboard

from services.dialog_state import dialog_state
from services.discount_service import DiscountService
from services.review_service import ReviewService

from services.admin_service import AdminService
from services.admin_catalog_service import AdminCatalogService
from keyboards.admin import (
    create_admin_categories_keyboard,
    create_admin_places_keyboard,
)


def register_dialog_handlers(bot: TeleBot) -> None:
    discount_service = DiscountService()
    review_service = ReviewService()
    admin_service = AdminService()
    catalog_service = AdminCatalogService()

    @bot.message_handler(commands=["cancel"])
    def cancel_dialog(message: Message) -> None:
        dialog_state.clear(
            message.chat.id,
            message.from_user.id,
        )

        bot.send_message(
            message.chat.id,
            "✅ Действие отменено.\n"
            "Отправь /start, чтобы открыть главное меню.",
        )

    @bot.message_handler(
        content_types=["text"],
        func=lambda message: (
                dialog_state.get(
                    message.chat.id,
                    message.from_user.id,
                ) is not None
                and not message.text.startswith("/")
        ),
    )
    def process_dialog(message: Message) -> None:
        state = dialog_state.get(
            message.chat.id,
            message.from_user.id,
        )

        if state is None:
            return

        action = state["action"]
        text = message.text.strip()

        if action.startswith("admin_"):
            if not admin_service.is_admin(message.from_user.id):
                dialog_state.clear(message.chat.id, message.from_user.id)
                bot.send_message(message.chat.id, "⛔ Доступ запрещён.")
                return

            if action == "admin_add_category":
                try:
                    category = catalog_service.add_category(text)
                except ValueError as error:
                    bot.send_message(message.chat.id, f"❌ {error}")
                    return

                dialog_state.clear(message.chat.id, message.from_user.id)

                bot.send_message(
                    message.chat.id,
                    f"✅ Категория «{category.name}» добавлена!",
                    reply_markup=create_admin_categories_keyboard(),
                )
                return

            if action == "admin_add_place":
                step = state["step"]
                data = state["data"].copy()

                if step == "name":
                    if not 1 <= len(text) <= 150:
                        bot.send_message(
                            message.chat.id,
                            "❌ Название должно содержать от 1 до 150 символов.",
                        )
                        return

                    data["name"] = text

                    dialog_state.set(
                        message.chat.id,
                        message.from_user.id,
                        {
                            "action": "admin_add_place",
                            "step": "address",
                            "data": data,
                        },
                    )

                    bot.send_message(
                        message.chat.id,
                        "📍 Введи адрес заведения:",
                    )
                    return

                if step == "address":
                    if not 1 <= len(text) <= 300:
                        bot.send_message(
                            message.chat.id,
                            "❌ Адрес должен содержать от 1 до 300 символов.",
                        )
                        return

                    data["address"] = text

                    dialog_state.set(
                        message.chat.id,
                        message.from_user.id,
                        {
                            "action": "admin_add_place",
                            "step": "latitude",
                            "data": data,
                        },
                    )

                    bot.send_message(
                        message.chat.id,
                        "🌍 Введи широту (например, 59.9343):",
                    )
                    return

                if step == "latitude":
                    try:
                        latitude = float(text.replace(",", "."))

                        if not -90 <= latitude <= 90:
                            raise ValueError

                    except ValueError:
                        bot.send_message(
                            message.chat.id,
                            "❌ Введи широту от -90 до 90.",
                        )
                        return

                    data["latitude"] = latitude

                    dialog_state.set(
                        message.chat.id,
                        message.from_user.id,
                        {
                            "action": "admin_add_place",
                            "step": "longitude",
                            "data": data,
                        },
                    )

                    bot.send_message(
                        message.chat.id,
                        "🌍 Введи долготу (например, 30.3351):",
                    )
                    return

                if step == "longitude":
                    try:
                        longitude = float(text.replace(",", "."))

                        if not -180 <= longitude <= 180:
                            raise ValueError

                    except ValueError:
                        bot.send_message(
                            message.chat.id,
                            "❌ Введи долготу от -180 до 180.",
                        )
                        return

                    try:
                        place = catalog_service.add_place(
                            name=data["name"],
                            address=data["address"],
                            latitude=data["latitude"],
                            longitude=longitude,
                        )
                    except ValueError as error:
                        bot.send_message(message.chat.id, f"❌ {error}")
                        return

                    dialog_state.clear(message.chat.id, message.from_user.id)

                    bot.send_message(
                        message.chat.id,
                        f"✅ Заведение «{place.name}» добавлено!\n"
                        f"📍 {place.address}",
                        reply_markup=create_admin_places_keyboard(),
                    )
                    return

            bot.send_message(
                message.chat.id,
                "❌ Неизвестное действие администратора.",
            )
            dialog_state.clear(message.chat.id, message.from_user.id)
            return

        # Поиск по названию
        if action == "search_name":
            if not text:
                bot.send_message(
                    message.chat.id,
                    "❌ Введи непустое название.",
                )
                return

            discounts = discount_service.search_discounts(text)

        # Поиск по проценту
        elif action == "search_percent":
            try:
                percent = int(text)

                if not 0 <= percent <= 100:
                    raise ValueError

            except ValueError:
                bot.send_message(
                    message.chat.id,
                    "❌ Введи целое число от 0 до 100.",
                )
                return

            discounts = discount_service.get_discounts_by_percent(
                percent
            )

        # Отзыв или жалоба
        elif action in ("review", "report"):
            if len(text) > 1000:
                bot.send_message(
                    message.chat.id,
                    "❌ Максимальная длина — 1000 символов.",
                )
                return

            try:
                if action == "review":
                    review_service.add_review(
                        telegram_id=message.from_user.id,
                        username=message.from_user.username,
                        discount_id=state["discount_id"],
                        rating=state["rating"],
                        comment="" if text == "-" else text,
                    )

                    response = "✅ Спасибо! Твой отзыв сохранён."

                else:
                    review_service.add_report(
                        telegram_id=message.from_user.id,
                        username=message.from_user.username,
                        discount_id=state["discount_id"],
                        reason=text,
                    )

                    response = "✅ Жалоба отправлена на рассмотрение."

            except ValueError as error:
                bot.send_message(
                    message.chat.id,
                    f"❌ {error}",
                )
                return

            dialog_state.clear(
                message.chat.id,
                message.from_user.id,
            )

            bot.send_message(
                chat_id=message.chat.id,
                text=response,
                reply_markup=create_reviews_keyboard(
                    state["discount_id"]
                ),
            )
            return

        else:
            return

        # Результаты поиска
        dialog_state.clear(
            message.chat.id,
            message.from_user.id,
        )

        if discounts:
            bot.send_message(
                chat_id=message.chat.id,
                text=f"🔎 Найдено скидок: {len(discounts)}",
                reply_markup=create_discounts_keyboard(discounts),
            )
        else:
            bot.send_message(
                chat_id=message.chat.id,
                text="😔 По твоему запросу ничего не найдено.",
                reply_markup=create_search_keyboard(),
            )
