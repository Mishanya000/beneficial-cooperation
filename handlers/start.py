from telebot import TeleBot
from telebot.types import Message

from keyboards.main_menu import create_main_menu
from services.dialog_state import dialog_state


def register_start_handlers(bot: TeleBot) -> None:

    @bot.message_handler(commands=["start"])
    def start_handler(message: Message) -> None:
        dialog_state.clear(
            message.chat.id,
            message.from_user.id,
        )

        text = (
            "👋 Привет!\n\n"
            "Добро пожаловать в бот студенческих скидок!\n\n"
            "Здесь ты можешь найти актуальные скидки "
            "в различных заведениях города.\n\n"
            "Выбери интересующий раздел 👇"
        )

        bot.send_message(
            chat_id=message.chat.id,
            text=text,
            reply_markup=create_main_menu(),
        )