from telebot import TeleBot
from telebot.types import Message

from keyboards.main_menu import create_main_menu
from keyboards.admin import create_admin_keyboard
from services.admin_service import AdminService
from services.dialog_state import dialog_state


def register_fallback_handlers(bot: TeleBot) -> None:
    admin_service = AdminService()

    @bot.message_handler(content_types=["text"])
    def handle_unexpected_text(message: Message) -> None:
        state = dialog_state.get(
            message.chat.id,
            message.from_user.id,
        )

        # Если бот ожидает текст в диалоге,
        # не отправляем сообщение-заглушку.
        if state is not None:
            return

        # Команды не считаем обычным текстом.
        if message.text.startswith("/"):
            return

        if admin_service.is_admin(message.from_user.id):
            bot.send_message(
                message.chat.id,
                "🤖 Я не умею отвечать на произвольные сообщения.\n\n"
                "Пожалуйста, выбери действие в меню 👇",
                reply_markup=create_admin_keyboard(),
            )
        else:
            bot.send_message(
                message.chat.id,
                "🤖 Я пока не умею поддерживать переписку.\n\n"
                "Пожалуйста, выбери интересующий раздел меню 👇",
                reply_markup=create_main_menu(),
            )