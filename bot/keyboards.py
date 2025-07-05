from aiogram.types import InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import MINIAPP_URL


def start_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Продолжить", callback_data="Continue"))
    builder.adjust(1)
    return builder.as_markup()


def main_menu(isRegister=False, lang="ru"):
    text = {
        "ru": ["Открыть софт", "Изменить язык", "Инструкция", "Политика пользования"],
        "en": ["Open Software", "Change Language", "Instructions", "Terms of Use"]
    }
    builder = InlineKeyboardBuilder()
    if isRegister:
        builder.row(InlineKeyboardButton(text=text[lang][0], web_app=WebAppInfo(url=MINIAPP_URL)))
    else:
        builder.row(InlineKeyboardButton(text=text[lang][0], callback_data="OpenSoft"))
    builder.row(InlineKeyboardButton(text=text[lang][1], callback_data="ChangeLang"))
    builder.row(InlineKeyboardButton(text=text[lang][2], callback_data="Instruction"))
    builder.row(InlineKeyboardButton(text=text[lang][3], callback_data="UserPolicy"))
    return builder.as_markup()


def language_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Русский", callback_data="lang_ru"),
        InlineKeyboardButton(text="English", callback_data="lang_en")
    )
    return builder.as_markup()


def admin_panel():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Открыть софт", web_app=WebAppInfo(url=MINIAPP_URL)))
    builder.row(InlineKeyboardButton(text="Мои данные", callback_data="MyAdminData"))
    builder.row(InlineKeyboardButton(text="Статистика", callback_data="Statistic"))
    builder.row(InlineKeyboardButton(text="Рассылка", callback_data="Mailing"))
    return builder.as_markup()
