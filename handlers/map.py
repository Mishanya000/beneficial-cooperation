from telebot import TeleBot
from telebot.types import CallbackQuery

from keyboards.map import create_places_keyboard
from services.place_service import PlaceService
from services.discount_service import DiscountService


def register_map_handlers(bot: TeleBot) -> None:
    place_service = PlaceService()
    discount_service = DiscountService()

    @bot.callback_query_handler(
        func=lambda call: call.data == "map"
    )
    def show_map(call: CallbackQuery) -> None:
        bot.answer_callback_query(call.id)

        places = place_service.get_places_with_discounts()

        if not places:
            bot.send_message(
                call.message.chat.id,
                "😔 Пока нет заведений с действующими скидками.",
            )
            return

        bot.send_message(
            chat_id=call.message.chat.id,
            text="🗺 Выбери заведение, чтобы посмотреть его на карте:",
            reply_markup=create_places_keyboard(places),
        )

    @bot.callback_query_handler(
        func=lambda call: call.data.startswith("place:")
    )
    def show_place_location(call: CallbackQuery) -> None:
        bot.answer_callback_query(call.id)

        place_id = int(call.data.split(":")[1])
        place = place_service.get_place(place_id)

        if place is None:
            bot.send_message(
                call.message.chat.id,
                "❌ Заведение не найдено.",
            )
            return

        bot.send_message(
            call.message.chat.id,
            f"📍 {place.name}\n{place.address}",
        )

        bot.send_location(
            chat_id=call.message.chat.id,
            latitude=place.latitude,
            longitude=place.longitude,
        )

    @bot.callback_query_handler(
        func=lambda call: call.data.startswith("location:")
    )
    def show_discount_location(call: CallbackQuery) -> None:
        bot.answer_callback_query(call.id)

        discount_id = int(call.data.split(":")[1])
        discount = discount_service.get_discount(discount_id)

        if discount is None:
            bot.send_message(
                call.message.chat.id,
                "❌ Скидка не найдена или больше не действует.",
            )
            return

        place = discount.place

        bot.send_message(
            call.message.chat.id,
            f"📍 {place.name}\n{place.address}",
        )

        bot.send_location(
            chat_id=call.message.chat.id,
            latitude=place.latitude,
            longitude=place.longitude,
        )