from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def start_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="Продолжить"))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def main_menu(lang="ru"):
    text = {
        "ru": ["Открыть софт", "Изменить язык", "Инструкция", "Политика пользования"],
        "en": ["Open Software", "Change Language", "Instructions", "Terms of Use"]
    }
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text=text[lang][0]))
    builder.row(KeyboardButton(text=text[lang][1]), KeyboardButton(text=text[lang][2]))
    builder.add(KeyboardButton(text=text[lang][3]))
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def language_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Русский", callback_data="lang_ru"),
        InlineKeyboardButton(text="English", callback_data="lang_en")
    )
    return builder.as_markup()


def admin_panel():
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(text="Мои данные"),
        KeyboardButton(text="Статистика"),
        KeyboardButton(text="Рассылка")
    )
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
