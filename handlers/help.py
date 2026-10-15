from telebot import TeleBot
from telebot.types import CallbackQuery

from keyboards.main_menu import create_main_menu


def register_help_handlers(bot: TeleBot) -> None:

    @bot.callback_query_handler(
        func=lambda call: call.data == "help"
    )
    def show_help(call: CallbackQuery) -> None:
        print("HELP CALLBACK:", call.data)

        bot.answer_callback_query(call.id)

        bot.send_message(
            call.message.chat.id,
            "🆘 Помощь\n\n"
            "Этот бот помогает студентам находить скидки.\n\n"
            "🔥 Скидки — доступные предложения.\n"
            "📂 Категории — скидки по категориям.\n"
            "🔎 Поиск — поиск по названию и проценту.\n"
            "🗺 Карта — расположение заведений.\n"
            "⭐ Отзывы — оценки и комментарии пользователей.\n\n"
            "Чтобы оставить отзыв или жалобу, открой карточку скидки.\n\n"
            "Для возврата в главное меню отправь /start.",
            reply_markup=create_main_menu(),
        )