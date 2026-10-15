
import logging

from telebot import TeleBot
from telebot.types import CallbackQuery

from keyboards.reviews import (
    create_rating_keyboard,
    create_reviews_keyboard,
    create_reviews_list_keyboard,
)
from services.dialog_state import dialog_state
from services.review_service import ReviewService
from services.discount_service import DiscountService


logger = logging.getLogger(__name__)


def register_review_handlers(bot: TeleBot) -> None:
    service = ReviewService()
    discount_service = DiscountService()

    # ==========================================
    # ГЛАВНАЯ КНОПКА "ОТЗЫВЫ"
    # ==========================================

    @bot.callback_query_handler(
        func=lambda call: call.data == "reviews"
    )
    def show_reviews_menu(call: CallbackQuery) -> None:
        print("1. КНОПКА ОТЗЫВЫ НАЖАТА")

        bot.answer_callback_query(call.id)

        try:
            discounts = discount_service.get_active_discounts()

            print("2. СКИДКИ ПОЛУЧЕНЫ:", len(discounts))

            if not discounts:
                bot.send_message(
                    call.message.chat.id,
                    "😔 Пока нет доступных скидок, "
                    "для которых можно посмотреть отзывы.",
                )
                return

            keyboard = create_reviews_list_keyboard(discounts)

            print("3. КЛАВИАТУРА СОЗДАНА")

            bot.send_message(
                chat_id=call.message.chat.id,
                text="⭐ Выбери скидку, чтобы посмотреть отзывы:",
                reply_markup=keyboard,
            )

            print("4. СООБЩЕНИЕ ОТПРАВЛЕНО")

        except Exception:
            logger.exception("Ошибка при открытии меню отзывов")

            bot.send_message(
                call.message.chat.id,
                "❌ Не удалось открыть отзывы. "
                "Попробуй ещё раз позже.",
            )

    # ==========================================
    # ПРОСМОТР ОТЗЫВОВ О СКИДКЕ
    # ==========================================

    @bot.callback_query_handler(
        func=lambda call: call.data.startswith("reviews:")
    )
    def show_reviews(call: CallbackQuery) -> None:
        bot.answer_callback_query(call.id)

        discount_id = int(call.data.split(":")[1])

        discount = discount_service.get_discount(discount_id)

        if discount is None:
            bot.send_message(
                call.message.chat.id,
                "❌ Скидка больше не доступна.",
            )
            return

        reviews, average = service.get_reviews(discount_id)

        text = f"⭐ Отзывы о скидке «{discount.title}»\n\n"

        if average is not None:
            text += f"Средняя оценка: {average:.1f}/5\n\n"
        else:
            text += "Пока оценок нет.\n\n"

        if not reviews:
            text += "Будь первым, кто оставит отзыв! 😊\n"
        else:
            for review in reviews:
                stars = "⭐" * review.rating
                comment = review.comment or "Без комментария"

                text += f"{stars}\n{comment}\n\n"

        text = text[:4000]

        bot.send_message(
            chat_id=call.message.chat.id,
            text=text,
            reply_markup=create_reviews_keyboard(discount_id),
        )

    # ==========================================
    # НАЧАЛО ДОБАВЛЕНИЯ ОТЗЫВА
    # ==========================================

    @bot.callback_query_handler(
        func=lambda call: call.data.startswith("review:add:")
    )
    def start_review(call: CallbackQuery) -> None:
        bot.answer_callback_query(call.id)

        discount_id = int(call.data.split(":")[2])

        if discount_service.get_discount(discount_id) is None:
            bot.send_message(
                call.message.chat.id,
                "❌ Скидка недоступна.",
            )
            return

        dialog_state.clear(
            call.message.chat.id,
            call.from_user.id,
        )

        bot.send_message(
            chat_id=call.message.chat.id,
            text="⭐ Выбери оценку от 1 до 5:",
            reply_markup=create_rating_keyboard(discount_id),
        )

    # ==========================================
    # ВЫБОР ОЦЕНКИ
    # ==========================================

    @bot.callback_query_handler(
        func=lambda call: call.data.startswith("review:rating:")
    )
    def select_rating(call: CallbackQuery) -> None:
        bot.answer_callback_query(call.id)

        parts = call.data.split(":")

        discount_id = int(parts[2])
        rating = int(parts[3])

        if discount_service.get_discount(discount_id) is None:
            bot.send_message(
                call.message.chat.id,
                "❌ Скидка недоступна.",
            )
            return

        if not 1 <= rating <= 5:
            bot.send_message(
                call.message.chat.id,
                "❌ Некорректная оценка.",
            )
            return

        dialog_state.set(
            call.message.chat.id,
            call.from_user.id,
            {
                "action": "review",
                "discount_id": discount_id,
                "rating": rating,
            },
        )

        bot.send_message(
            call.message.chat.id,
            "✍️ Напиши отзыв о скидке.\n\n"
            "Если не хочешь оставлять комментарий, "
            "отправь символ «-».\n\n"
            "Для отмены отправь /cancel",
        )

    # ==========================================
    # ОТПРАВКА ЖАЛОБЫ
    # ==========================================

    @bot.callback_query_handler(
        func=lambda call: call.data.startswith("report:add:")
    )
    def start_report(call: CallbackQuery) -> None:
        bot.answer_callback_query(call.id)

        discount_id = int(call.data.split(":")[2])

        if discount_service.get_discount(discount_id) is None:
            bot.send_message(
                call.message.chat.id,
                "❌ Скидка недоступна.",
            )
            return

        dialog_state.set(
            call.message.chat.id,
            call.from_user.id,
            {
                "action": "report",
                "discount_id": discount_id,
            },
        )

        bot.send_message(
            call.message.chat.id,
            "🚩 Опиши, почему скидка не работает.\n\n"
            "Например: «Заведение больше не предоставляет "
            "скидку по студенческому билету».\n\n"
            "Для отмены отправь /cancel",
        )
