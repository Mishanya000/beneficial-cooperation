from telebot import TeleBot
from telebot.types import CallbackQuery

from keyboards.admin import (
    create_admin_keyboard,
    create_admin_reports_keyboard,
    create_admin_report_actions_keyboard,
)
from services.admin_service import AdminService
from services.admin_report_service import AdminReportService


def register_admin_report_handlers(bot: TeleBot) -> None:
    admin_service = AdminService()
    report_service = AdminReportService()

    def check_admin(call: CallbackQuery) -> bool:
        if not admin_service.is_admin(call.from_user.id):
            bot.answer_callback_query(
                call.id,
                "⛔ Доступ запрещён.",
                show_alert=True,
            )
            return False

        bot.answer_callback_query(call.id)
        return True

    @bot.callback_query_handler(
        func=lambda call: call.data == "admin:reports"
    )
    def show_reports(call: CallbackQuery) -> None:
        if not check_admin(call):
            return

        reports = report_service.get_pending_reports()

        if not reports:
            bot.send_message(
                call.message.chat.id,
                "✅ Необработанных жалоб нет!",
                reply_markup=create_admin_keyboard(),
            )
            return

        bot.send_message(
            call.message.chat.id,
            f"🚩 Жалобы на рассмотрении: {len(reports)}",
            reply_markup=create_admin_reports_keyboard(reports),
        )

    @bot.callback_query_handler(
        func=lambda call: call.data.startswith("admin:report:view:")
    )
    def view_report(call: CallbackQuery) -> None:
        if not check_admin(call):
            return

        report_id = int(call.data.split(":")[-1])
        report = report_service.get_report(report_id)

        if report is None:
            bot.send_message(
                call.message.chat.id,
                "❌ Жалоба не найдена.",
            )
            return

        text = (
            f"🚩 Жалоба #{report.id}\n\n"
            f"🔥 Скидка: {report.discount.title}\n"
            f"📋 Причина: {report.reason}\n"
            f"📊 Статус: {report.status}\n"
            f"📅 Дата: {report.created_at:%d.%m.%Y %H:%M}"
        )

        if report.status != "pending":
            bot.send_message(
                call.message.chat.id,
                text + "\n\nЭта жалоба уже обработана.",
            )
            return

        bot.send_message(
            call.message.chat.id,
            text,
            reply_markup=create_admin_report_actions_keyboard(report.id),
        )

    @bot.callback_query_handler(
        func=lambda call: call.data.startswith("admin:report:resolve:")
    )
    def resolve_report(call: CallbackQuery) -> None:
        if not check_admin(call):
            return

        report_id = int(call.data.split(":")[-1])

        try:
            report_service.resolve_report(report_id)
        except ValueError as error:
            bot.send_message(call.message.chat.id, f"❌ {error}")
            return

        bot.send_message(
            call.message.chat.id,
            "✅ Жалоба принята. Скидка отключена.",
            reply_markup=create_admin_reports_keyboard(
                report_service.get_pending_reports()
            ),
        )

    @bot.callback_query_handler(
        func=lambda call: call.data.startswith("admin:report:reject:")
    )
    def reject_report(call: CallbackQuery) -> None:
        if not check_admin(call):
            return

        report_id = int(call.data.split(":")[-1])

        try:
            report_service.reject_report(report_id)
        except ValueError as error:
            bot.send_message(call.message.chat.id, f"❌ {error}")
            return

        bot.send_message(
            call.message.chat.id,
            "❌ Жалоба отклонена.",
            reply_markup=create_admin_reports_keyboard(
                report_service.get_pending_reports()
            ),
        )