from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import db, config, utils
from config import POSTBACK_CHANNEL_ID, IMG_START, INSTRUCTION, CHANGE_LANG, OPEN_SOFT, MAIN_MENU
from filters import IsAdmin
from handler_utils import *
from keyboards import *

router = Router()

dict_text = {
    "ru": {
        'select_action': "Выберите действие:",
        'select_lang': 'Выберите язык:',
        'access_denied': "<b>Регистрация не пройдена!</b>\n\n● После завершения регистрации, Вам автоматически придет уведомление в бота.\n\nНе забудь указать промокод, для лучшей синхронизации данных \n\nПРОМОКОД: {promoCode}",
        'access_granted': "✅ Доступ открыт! ",
        'instruction': "👋 Меня зовут Кортес. Я и моя команда разработали софт, которым пользуются топовые стримеры: *EVELONE, Mellstroy, MOCRIVSKY, Zubareff* и другие.\n\n"
                       "🎯 Он помогает выигрывать в прямом эфире, что привлекает новую аудиторию. Софт привязывается к вашему аккаунту 1WIN через хэш-коды и внутренние скрипты платформы.\n\n"
                       "📊 Статистика пользователей говорит сама за себя — стабильный рост выигрышей и высокая точность сигналов.\n\n"
                       "🚀 *Как начать работать с софтом:*\n\n"
                       "1️⃣ Зарегистрируйтесь через нашего бота (даже если уже есть аккаунт — нужен новый).\n"
                       "2️⃣ Выберите нужный слот:\n"
                       "• из списка прогретых 🔥\n"
                       "• через поиск 🔎\n"
                       "• из топа пользователей 👥\n"
                       "3️⃣ Загрузите скриншот или фото слота 🖼️\n"
                       "4️⃣ Нажмите “Анализ” — получите сигнал 🎯\n"
                       "5️⃣ Следуйте инструкции — например:\n"
                       "_“Бонус через 20 спинов, шанс 88%”_ → делаем 19 спинов по минималке и на 20-м повышаем ставку 💸\n\n"
        ,

        'hello': "🔥 Добро пожаловать в закрытую систему от Кортеса!\n\n"
                 "Здесь — софт, который используют топовые стримеры, чтобы выигрывать в прямом эфире и забирать жирные бонусы 💸\n\n"
                 "Готов подключиться к инсайду? Жми на кнопку ниже 👇",
    },
    "en": {
        'select_action': "Select an action:",
        'select_lang': 'Select language:',
        'access_denied': "<b>Registration not completed!</b>\n\n● Once registration is completed, you will automatically receive a notification from the bot.\n\nPROMOCODE: {promoCode}",
        'access_granted': "✅ Access granted! <a href='https://example.com'>Open Software</a>",
        'instruction': "👋 My name is Cortez. My team and I have developed software that is used by top streamers: *EVELONE, Mellstroy, MOCRIVSKY, Zubareff* and others.\n\n"
                       "🎯 It helps you win live, which attracts a new audience. The software is linked to your 1WIN account through hash codes and internal platform scripts.\n\n"
                       "📊 User statistics speak for themselves — a steady increase in winnings and high signal accuracy.\n\n"
                       "🚀 *How to start working with the software:*\n\n"
                       "1️⃣ Register through our bot (even if you already have an account, you'll need a new one).\n"
                       "2️⃣ Select the desired slot:\n"
                       "• from the list of warmed-up 🔥\n"
                       "• via search 🔎\n"
                       "• from the top of users 👥\n"
                       "3️⃣ Upload a screenshot or photo of the slot 🖼️\n"
                       "4️⃣ Click “Analysis” and receive a signal 🎯\n"
                       "5️⃣ Follow the instructions, for example:\n"
                       "_“Bonus after 20 spins, 88% chance”_ → make 19 spins at the minimum and increase the bet on the 20th spin 💸\n\n",
        'hello': "🔥 Welcome to the private system from Cortez!\n\n"
                 "Here is the software that top streamers use to win live streams and earn big bonuses 💸\n\n"
                 "Ready to join the insider? Click on the button below 👇"
    }
}


@router.message(F.text == "/start")
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    if message.from_user.id == config.ADMIN_ID:
        await admin_entry(message=message)
        return
    user = db.get_user(message.from_user.id)
    if not user:
        db.add_user(message.from_user.id)
    lang = db.get_language(message.from_user.id)

    await safe_send_photo(
        event=message,
        photo=IMG_START,
        caption=dict_text[lang]['hello'],
        reply_markup=start_keyboard()
    )


@router.callback_query(F.data == "Continue")
async def continue_handler(event: CallbackQuery):
    await safe_answer(event)
    await safe_delete(event)
    lang = db.get_language(event.from_user.id)
    await safe_send_photo(
        event=event,
        photo=MAIN_MENU,
        caption=dict_text[lang]['select_action'],
        reply_markup=main_menu(db.is_registered(event.from_user.id), lang)
    )


@router.callback_query(F.data == "ChangeLang")
async def change_language(event: CallbackQuery):
    await safe_answer(event)
    await safe_delete(event)
    lang = db.get_language(event.from_user.id)
    await safe_send_photo(
        event=event,
        photo=CHANGE_LANG,
        caption=dict_text[lang]['select_lang'],
        reply_markup=language_keyboard()
    )


@router.callback_query(F.data.startswith("lang_"))
async def set_language(event: CallbackQuery):
    await safe_answer(event)
    await safe_delete(event)
    lang = event.data.split("_")[1]
    db.update_language(event.from_user.id, lang)
    await safe_send_photo(
        event=event,
        photo=MAIN_MENU,
        caption=dict_text[lang]['select_action'],
        reply_markup=main_menu(db.is_registered(event.from_user.id), lang)
    )


@router.callback_query(F.data == "Instruction")
async def instructions(event: CallbackQuery):
    await safe_delete(event)
    await safe_answer(event)

    lang = db.get_language(event.from_user.id)
    await safe_send_photo(
        event=event,
        photo=INSTRUCTION,
        caption=dict_text[lang]['instruction'],
        reply_markup=main_menu(db.is_registered(event.from_user.id), lang)
    )


@router.callback_query(F.data == "OpenSoft")
async def open_software(event: CallbackQuery):
    await safe_answer(event)
    await safe_delete(event)
    ref_link, promo = db.get_settings()

    user_id = event.from_user.id
    lang = db.get_language(user_id)
    if not utils.check_registration(user_id):
        await safe_send_photo(
            event=event,
            photo=OPEN_SOFT,
            caption=dict_text[lang]['access_denied'].format(promoCode=promo),
            reply_markup=register(lang=lang, user_tg_id=event.from_user.id, reflink=ref_link)
        )
        return

    await safe_send_photo(
        event=event,
        photo=OPEN_SOFT,
        caption=dict_text[lang]['access_granted'],
        reply_markup=open_soft(lang)
    )


@router.message(F.text == "/admin", IsAdmin())
async def admin_entry(message: Message):
    await message.answer("Панель админа:", reply_markup=admin_panel())


@router.callback_query(F.data == "MyAdminData", IsAdmin())
async def my_data(event: CallbackQuery, state: FSMContext):
    await state.clear()
    ref_link, promo = db.get_settings()
    await safe_answer(event)
    await safe_edit_text(
        event,
        text=f"🔗 Реф.ссылка:\n{ref_link}\n\n🎁 Промокод:\n{promo}",
        reply_markup=admin_panel()
    )


@router.callback_query(F.data == "Statistic", IsAdmin())
async def stats(event: CallbackQuery, state: FSMContext):
    await state.clear()
    total, reg, dep, block = db.get_stats()
    await safe_answer(event)
    await safe_edit_text(
        event,
        f"👥 Всего пользователей: {total}\n✅ Зарегистрированы: {reg}\n💰 С депозитом: {dep}\n❌ Заблокировали бота: {block}",
        reply_markup=admin_panel()
    )


class Mailing(StatesGroup):
    message = State()


@router.callback_query(F.data == "Mailing", IsAdmin())
async def broadcast_prompt(event: CallbackQuery, state: FSMContext):
    await state.clear()
    await safe_answer(event)
    await safe_edit_text(event, "Пришли текст для рассылки.")
    await state.set_state(Mailing.message)


@router.message(Mailing.message, IsAdmin())
async def broadcast_send(message: types.Message, state: FSMContext):
    await state.clear()
    try:
        cursor = db.conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE blocked = 0")
        users = cursor.fetchall()
        cursor.close()
        send, not_send = await safe_send_all(
            text=message.text,
            users=users
        )

        await message.answer(
            text=f"Рассылка завершена.\n\nУведомление:\nПолучили: {send}\nНе получили: {not_send}",
            reply_markup=admin_panel()
        )
    except Exception as e:
        print(e)
        await message.answer(
            text=f"Ошибка при подключении к БД: {e}",
            reply_markup=admin_panel()
        )


class DataToUpdate(StatesGroup):
    update = State()


@router.callback_query(F.data == "UpdateAdminData", IsAdmin())
async def start_update_data(event: CallbackQuery, state: FSMContext):
    await state.clear()
    await safe_answer(event)
    await safe_edit_text(event, text="Выбери данные для обновления", reply_markup=data_to_update())


@router.callback_query(F.data.startswith("UpdateTo:"), IsAdmin())
async def select_option_update(event: CallbackQuery, state: FSMContext):
    await safe_answer(event)
    param = event.data.split(":")[1]
    await state.update_data(param=param)

    if param == "ref_link":
        await safe_edit_text(event, text="Отправь новую реферальную ссылку")
    elif param == "promo_code":
        await safe_edit_text(event, text="Отправь новый промокод")

    await state.set_state(DataToUpdate.update)


@router.message(DataToUpdate.update, IsAdmin())
async def update_admin(event: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    value = event.text
    updated = db.update(param=data['param'], value=value)
    if not updated:
        await event.answer(
            text="При обвновлении данных что-то пошло не так",
            reply_markup=admin_panel()
        )
        return

    if data['param'] == 'ref_link':
        await event.answer(
            text=f"Реф. ссылка успешно изменена!\n\nТекущая реф. ссылка: {event.text}",
            reply_markup=admin_panel()
        )
    elif data['param'] == 'promo_code':
        await event.answer(
            text=f"Промокод успешно изменен!\n\nТекущий промокод: {event.text}",
            reply_markup=admin_panel()
        )


@router.channel_post(F.chat.id == int(POSTBACK_CHANNEL_ID), IsAdmin())
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
            lang = db.get_language(user_id)
            try:
                await bot.send_photo(
                    chat_id=user_id,
                    photo=FSInputFile(path=OPEN_SOFT),
                    caption=dict_text[lang]['access_granted'],
                    reply_markup=open_soft(lang=lang)
                )
            except Exception as e:
                print(e)

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
