from aiogram.types import InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import CHANNEL_URL
from config import MINIAPP_URL


def start_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Продолжить ✅", callback_data="Continue"))
    builder.adjust(1)
    return builder.as_markup()


def main_menu(isRegister=False, lang="ru"):
    text = {
        "ru": ["🚀 Открыть софт 🚀", "🌍 Изменить язык 🌍", "📘 Инструкция 📘", "📢 Telegram-канал 📢"],
        "en": ["🚀 Open Software 🚀", "🌍 Change Language 🌍", "📘 Instructions 📘", "📢 Telegram Channel 📢"]
    }
    builder = InlineKeyboardBuilder()
    if isRegister:
        builder.row(InlineKeyboardButton(text=text[lang][0], web_app=WebAppInfo(url=MINIAPP_URL)))
    else:
        builder.row(InlineKeyboardButton(text=text[lang][0], callback_data="OpenSoft"))
    builder.row(InlineKeyboardButton(text=text[lang][1], callback_data="ChangeLang"))
    builder.row(InlineKeyboardButton(text=text[lang][2], callback_data="Instruction"))
    builder.row(InlineKeyboardButton(text=text[lang][3], url=CHANNEL_URL))
    return builder.as_markup()


def language_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Русский", callback_data="lang_ru"),
        InlineKeyboardButton(text="English", callback_data="lang_en")
    )
    return builder.as_markup()


def open_soft(lang='ru'):
    text = {
        "ru": {
            'open': "🚀 Открыть софт 🚀",
            'back': "🔙 Назад"
        },
        "en": {
            'open': "🚀 Open Software 🚀",
            'back': "🔙 Back"
        }
    }
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=text[lang]['open'], web_app=WebAppInfo(url=MINIAPP_URL)))
    builder.row(InlineKeyboardButton(text=text[lang]['back'], callback_data="Continue"))
    return builder.as_markup()


def register(lang, user_tg_id, reflink):
    text = {
        "ru": {
            'open': "💻 Зарегистрироваться",
            'back': "🔙 Назад"
        },
        "en": {
            'open': "💻 Register",
            'back': "🔙 Back"
        }
    }
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=text[lang]['open'], url=f"{reflink}&sub1={user_tg_id}"))
    builder.row(InlineKeyboardButton(text=text[lang]['back'], callback_data="Continue"))
    return builder.as_markup()


def admin_panel():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Открыть софт", web_app=WebAppInfo(url=MINIAPP_URL)))
    builder.row(InlineKeyboardButton(text="Мои данные", callback_data="MyAdminData"))
    builder.row(InlineKeyboardButton(text="Статистика", callback_data="Statistic"))
    builder.row(InlineKeyboardButton(text="Рассылка", callback_data="Mailing"))
    builder.row(InlineKeyboardButton(text="Обновить данные", callback_data="UpdateAdminData"))
    return builder.as_markup()


def data_to_update():
    return (
        InlineKeyboardBuilder()
        .row(InlineKeyboardButton(text="Реф.ссылка", callback_data="UpdateTo:ref_link"), width=1)
        .row(InlineKeyboardButton(text="Промокод", callback_data="UpdateTo:promo_code"), width=1)
    ).as_markup()
