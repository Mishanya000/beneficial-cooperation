from telebot import TeleBot
from telebot.types import CallbackQuery

from keyboards.discounts import (
    create_discount_details_keyboard,
    create_discounts_keyboard,
)
from keyboards.main_menu import create_main_menu

from services.dialog_state import dialog_state
from services.discount_service import DiscountService


def register_discount_handlers(bot: TeleBot) -> None:
    service = DiscountService()

    @bot.callback_query_handler(
        func=lambda call: call.data == "discounts"
    )
    def show_discounts(call: CallbackQuery) -> None:
        bot.answer_callback_query(call.id)

        discounts = service.get_active_discounts()

        if not discounts:
            bot.send_message(
                call.message.chat.id,
                "😔 Пока нет действующих скидок.",
            )
            return

        bot.send_message(
            chat_id=call.message.chat.id,
            text="🔥 Актуальные скидки:",
            reply_markup=create_discounts_keyboard(discounts),
        )

    @bot.callback_query_handler(
        func=lambda call: call.data.startswith("discount:")
    )
    def show_discount_details(call: CallbackQuery) -> None:
        bot.answer_callback_query(call.id)

        discount_id = int(call.data.split(":")[1])
        discount = service.get_discount(discount_id)

        if discount is None:
            bot.send_message(
                call.message.chat.id,
                "❌ Скидка не найдена или больше не действует.",
            )
            return

        percent = (
            f"{discount.discount_percent}%"
            if discount.discount_percent is not None
            else "Специальное предложение"
        )

        valid_until = (
            discount.valid_until.strftime("%d.%m.%Y")
            if discount.valid_until is not None
            else "Бессрочно"
        )

        text = (
            f"🔥 {discount.title}\n\n"
            f"🏪 Заведение: {discount.place.name}\n"
            f"📂 Категория: {discount.category.name}\n"
            f"💰 Скидка: {percent}\n"
            f"📍 Адрес: {discount.place.address}\n\n"
            f"📝 Описание:\n{discount.description}\n\n"
            f"📋 Условия:\n{discount.conditions}\n\n"
            f"📅 Действует до: {valid_until}"
        )

        bot.send_message(
            chat_id=call.message.chat.id,
            text=text,
            reply_markup=create_discount_details_keyboard(
                discount.id
            ),
        )

    @bot.callback_query_handler(
        func=lambda call: call.data == "main_menu"
    )
    def show_main_menu(call: CallbackQuery) -> None:
        bot.answer_callback_query(call.id)

        dialog_state.clear(
            call.message.chat.id,
            call.from_user.id,
        )

        bot.send_message(
            chat_id=call.message.chat.id,
            text="🏠 Главное меню:",
            reply_markup=create_main_menu(),
        )