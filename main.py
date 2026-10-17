import telebot

from config import BOT_TOKEN
from database import init_db

from handlers.start import register_start_handlers
from handlers.discounts import register_discount_handlers
from handlers.categories import register_category_handlers
from handlers.search import register_search_handlers
from handlers.map import register_map_handlers
from handlers.reviews import register_review_handlers
from handlers.dialogs import register_dialog_handlers
from handlers.admin import register_admin_handlers
from handlers.admin_discounts import register_admin_discount_handlers
from handlers.admin_reports import register_admin_report_handlers
from handlers.help import register_help_handlers


def main() -> None:
    init_db()

    bot = telebot.TeleBot(BOT_TOKEN)

    register_start_handlers(bot)
    register_discount_handlers(bot)
    register_category_handlers(bot)
    register_search_handlers(bot)
    register_map_handlers(bot)
    register_review_handlers(bot)

    register_admin_discount_handlers(bot)
    register_admin_report_handlers(bot)
    register_admin_handlers(bot)

    register_dialog_handlers(bot)

    register_review_handlers(bot)
    register_help_handlers(bot)

    print("Database initialized!")
    print("Bot started successfully!")

    bot.infinity_polling(skip_pending=True)


if __name__ == "__main__":
    main()