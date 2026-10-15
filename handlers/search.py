from telebot import TeleBot
from telebot.types import CallbackQuery

from keyboards.search import create_search_keyboard
from services.dialog_state import dialog_state


def register_search_handlers(bot: TeleBot) -> None:

    @bot.callback_query_handler(
        func=lambda call: call.data == "search"
    )
    def show_search_menu(call: CallbackQuery) -> None:
        bot.answer_callback_query(call.id)

        dialog_state.clear(
            call.message.chat.id,
            call.from_user.id,
        )

        bot.send_message(
            chat_id=call.message.chat.id,
            text="🔎 Выбери способ поиска:",
            reply_markup=create_search_keyboard(),
        )

    @bot.callback_query_handler(
        func=lambda call: call.data == "search:name"
    )
    def search_by_name(call: CallbackQuery) -> None:
        bot.answer_callback_query(call.id)

        dialog_state.set(
            call.message.chat.id,
            call.from_user.id,
            {"action": "search_name"},
        )

        bot.send_message(
            call.message.chat.id,
            "🏪 Введи название скидки или заведения:\n\n"
            "Для отмены отправь /cancel",
        )

    @bot.callback_query_handler(
        func=lambda call: call.data == "search:percent"
    )
    def search_by_percent(call: CallbackQuery) -> None:
        bot.answer_callback_query(call.id)

        dialog_state.set(
            call.message.chat.id,
            call.from_user.id,
            {"action": "search_percent"},
        )

        bot.send_message(
            call.message.chat.id,
            "💰 Введи минимальный процент скидки (0–100):\n\n"
            "Для отмены отправь /cancel",
        )