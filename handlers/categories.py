from telebot import TeleBot
from telebot.types import CallbackQuery

from keyboards.categories import create_categories_keyboard
from keyboards.discounts import create_discounts_keyboard
from services.category_service import CategoryService
from services.discount_service import DiscountService


def register_category_handlers(bot: TeleBot) -> None:
    category_service = CategoryService()
    discount_service = DiscountService()

    @bot.callback_query_handler(
        func=lambda call: call.data == "categories"
    )
    def show_categories(call: CallbackQuery) -> None:
        bot.answer_callback_query(call.id)

        categories = category_service.get_categories()

        bot.send_message(
            chat_id=call.message.chat.id,
            text="📂 Выбери категорию:",
            reply_markup=create_categories_keyboard(categories),
        )

    @bot.callback_query_handler(
        func=lambda call: call.data.startswith("category:")
    )
    def show_category_discounts(call: CallbackQuery) -> None:
        bot.answer_callback_query(call.id)

        category_id = int(call.data.split(":")[1])

        discounts = discount_service.get_discounts_by_category(
            category_id
        )

        if not discounts:
            bot.send_message(
                chat_id=call.message.chat.id,
                text="😔 В этой категории пока нет скидок.",
                reply_markup=create_categories_keyboard(
                    category_service.get_categories()
                ),
            )
            return

        bot.send_message(
            chat_id=call.message.chat.id,
            text="🔥 Скидки в выбранной категории:",
            reply_markup=create_discounts_keyboard(discounts),
        )