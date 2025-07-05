from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from bot import db, config, utils
from bot.config import POSTBACK_CHANNEL_ID
from create import bot
from keyboards import *

router = Router()


@router.message(F.text == "/start")
async def start_handler(message: Message):
    if message.from_user.id == config.ADMIN_ID:
        await admin_entry(message=message)
        return
    db.add_user(message.from_user.id)
    lang = db.get_language(message.from_user.id)
    text = {
        "ru": "👋 Добро пожаловать!\nНажмите кнопку ниже, чтобы продолжить.",
        "en": "👋 Welcome!\nPress the button below to continue."
    }
    # await bot.send_photo(
    #     photo=FSInputFile(path="Тут путь до фотки"),
    #     caption=text[lang],
    #     reply_markup=start_keyboard()
    # ) <-- Пример добавления фотографии к посту

    await message.answer(text[lang], reply_markup=start_keyboard())


@router.callback_query(F.data == "Continue")
async def continue_handler(event: CallbackQuery):
    lang = db.get_language(event.from_user.id)
    text = {
        "ru": "Выберите действие:",
        "en": "Select an action:"
    }
    await event.answer()
    await event.message.edit_text(text[lang], reply_markup=main_menu(db.is_registered(event.from_user.id), lang))


@router.callback_query(F.data == "ChangeLang")
async def change_language(event: CallbackQuery):
    await event.answer()
    await event.message.edit_text("Выберите язык:", reply_markup=language_keyboard())


@router.callback_query(F.data.startswith("lang_"))
async def set_language(event: CallbackQuery):
    lang = event.data.split("_")[1]
    db.update_language(event.from_user.id, lang)
    await event.answer()
    await event.message.edit_text(
        text="Язык изменён\n\nВыберите действие:",
        reply_markup=main_menu(db.is_registered(event.from_user.id), lang)
    )


@router.callback_query(F.data == "Instruction")
async def instructions(event: CallbackQuery):
    lang = db.get_language(event.from_user.id)
    text = {
        "ru": "📘 Инструкция:\n1. Зарегистрируйтесь по ссылке.\n2. Введите промокод.\n3. Запустите мини-апп.",
        "en": "📘 Instructions:\n1. Register via the link.\n2. Enter the promo code.\n3. Launch the mini app."
    }
    await event.answer()
    await event.message.answer(text=text[lang], reply_markup=main_menu(db.is_registered(event.from_user.id), lang))


@router.callback_query(F.data == "UserPolicy")
async def terms(event: CallbackQuery):
    lang = db.get_language(event.from_user.id)
    text = {
        "ru": "⚖ Политика пользования:\nЭто шаблон политики.",
        "en": "⚖ Terms of Use:\nThis is a terms template."
    }
    await event.answer()
    await event.message.edit_text(text=text[lang], reply_markup=main_menu(db.is_registered(event.from_user.id), lang))


@router.callback_query(F.data == "OpenSoft")
async def open_software(event: CallbackQuery):
    user_id = event.from_user.id
    lang = db.get_language(user_id)
    await event.answer()
    if utils.check_registration(user_id):
        text = {
            "ru": "✅ Доступ открыт! [Запустить софт](https://example.com)",
            "en": "✅ Access granted! [Open Software](https://example.com)"
        }
        await event.message.edit_text(text[lang], reply_markup=main_menu(db.is_registered(event.from_user.id), lang))
    else:
        text = {
            "ru": "🚫 Необходимо зарегистрироваться по реферальной ссылке.",
            "en": "🚫 You need to register via the referral link."
        }
        ref_link, promo = db.get_settings()
        await event.message.edit_text(f"{text[lang]}\n\n🔗 {ref_link}\n\n🎁 Промокод: {promo}",
                                      reply_markup=main_menu(db.is_registered(event.from_user.id), lang))


@router.message(F.from_user.id == config.ADMIN_ID, F.text == "/admin")
async def admin_entry(message: Message):
    await message.answer("Панель админа:", reply_markup=admin_panel())


@router.callback_query(F.from_user.id == config.ADMIN_ID, F.data == "MyAdminData")
async def my_data(event: CallbackQuery):
    ref_link, promo = db.get_settings()
    await event.answer()
    await event.message.edit_text(
        f"🔗 Реф.ссылка:\n{ref_link}\n\n🎁 Промокод:\n{promo}",
        reply_markup=admin_panel()
    )


@router.callback_query(F.from_user.id == config.ADMIN_ID, F.data == "Statistic")
async def stats(event: CallbackQuery):
    total, reg, dep, block = db.get_stats()
    await event.answer()
    await event.message.edit_text(
        f"👥 Всего пользователей: {total}\n✅ Зарегистрированы: {reg}\n💰 С депозитом: {dep}\n❌ Заблокировали бота: {block}",
        reply_markup=admin_panel()
    )


class Mailing(StatesGroup):
    message = State()


@router.callback_query(F.from_user.id == config.ADMIN_ID, F.data == "Mailing")
async def broadcast_prompt(event: CallbackQuery, state: FSMContext):
    await event.answer()
    await event.message.edit_text("Пришли текст для рассылки.")
    await state.set_state(Mailing.message)


@router.message(F.from_user.id == config.ADMIN_ID, Mailing.message)
async def broadcast_send(message: types.Message, state: FSMContext):
    text = message.text
    try:
        cursor = db.conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE blocked = 0")
        users = cursor.fetchall()
        cursor.close()
        for u in users:
            try:
                await bot.send_message(u[0], text)
            except Exception as e:
                print(e)
                db.set_blocked(u[0])
        await message.answer("Рассылка завершена.", reply_markup=admin_panel())
    except Exception as e:
        print(e)
        await message.answer(f"Ошибка при подключении к БД: {e}", reply_markup=admin_panel())
    await state.clear()


@router.channel_post(F.chat.id == int(POSTBACK_CHANNEL_ID))
async def postback_handler(event: Message):
    try:
        text = event.text
        if '|' not in text and 'Firstdep' not in text:
            user_id = int(text)
            user = db.get_user(user_id)
            if not user:
                db.add_user(user_id)
            db.set_registered(user_id)
            await bot.send_message(
                chat_id=POSTBACK_CHANNEL_ID,
                text=f"<strong>✅ РЕГИСТРАЦИЯ ✅</strong>\n\n"
                     f"🧑🏻‍💻: {user_id}\n"
                     f"Прошел регистрацию по Вашей реферальной ссылке!"
            )
        elif '|' in text and len(text.split('|')) and 'Firstdep' not in text:
            parts = text.split('|')

            user_id = int(parts[0].strip())
            country = str(parts[1].strip())
            amount = float(parts[2].strip())
            await bot.send_message(
                chat_id=POSTBACK_CHANNEL_ID,
                text=f"<strong>💵 ДЕПОЗИТ 💵</strong>\n\n"
                     f"🧑🏻‍💻: {user_id} [Нет в базе]\n"
                     f"🗺: {country}\n"
                     f"💵: {amount}",
            )
        elif '|' in text and 'Firstdep' in text:
            parts = text.split('|')
            user_id = int(parts[0].strip())
            amount = float(parts[2].strip())
            dep = db.get_deposit(user_id)
            if dep is None:
                db.update_deposited(user_id)
                await bot.send_message(
                    chat_id=POSTBACK_CHANNEL_ID,
                    text=f"<strong>🔥 ПЕРВЫЙ ДЕПОЗИТ 🔥</strong>\n\n"
                         f"🧑🏻‍💻: {user_id} [Нет в базе]\n"
                         f"💵: {amount}",
                )
                return
            await bot.send_message(
                chat_id=POSTBACK_CHANNEL_ID,
                text=f"<strong>Пользователь {user_id} уже делал первый депозит</strong>"
            )

    except Exception as e:
        await event.reply(f"❌ Ошибка обработки: {str(e)}")
