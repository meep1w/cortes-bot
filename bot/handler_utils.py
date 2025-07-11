import logging

from aiogram import exceptions
from aiogram.types import CallbackQuery, Message, FSInputFile

from create import bot

logger = logging.getLogger(__name__)


# async def edit_and_answer(event: CallbackQuery, text, reply_markup=None):
#     await safe_answer(event)
#     await safe_edit_text(event, text, reply_markup)
#
#
# async def clear_and_edit(
#         event: CallbackQuery,
#         state: FSMContext = None,
#         text: str = None,
#         reply_markup: Optional[ReplyMarkupUnion] = None
# ):
#     await safe_answer(event)
#     if state:
#         await state.clear()
#     await safe_edit_text(event=event, text=text, reply_markup=reply_markup)


async def safe_send_photo(event: CallbackQuery | Message, photo, caption, reply_markup):
    try:
        await bot.send_photo(
            chat_id=event.from_user.id,
            photo=FSInputFile(path=photo),
            caption=caption,
            reply_markup=reply_markup
        )
    except Exception as e:
        print(e)


async def safe_edit_text(event: CallbackQuery, text, reply_markup=None):
    try:
        await event.message.edit_text(text=text, reply_markup=reply_markup)
    except exceptions.TelegramBadRequest as tg:
        if "message is not modified" in str(tg):
            pass
        if "query is too old" in str(tg) or "query ID is invalid" in str(tg):
            pass
        else:
            logger.error(tg)
    except Exception as e:
        logger.error(e)


async def safe_send(chat_id, text, reply_markup=None):
    try:
        await bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=reply_markup
        )
        return True
    except Exception as e:
        logger.error(e)
        return False


async def safe_send_all(text, users, reply_markup=None):
    send, not_send = 0, 0
    for user_id in users:
        was_send = await safe_send(user_id[0], text, reply_markup)
        if was_send:
            send += 1
        else:
            not_send += 1
    return send, not_send


# async def safe_send_copy(chat_id, from_chat, message):
#     try:
#         await bot.copy_message(
#             chat_id=chat_id,
#             from_chat_id=from_chat,
#             message_id=message
#         )
#         return True
#     except Exception as e:
#         logger.error(e)
#         return False
#
#
# async def safe_send_copy_all(from_chat, message, users):
#     send, not_send = 0, 0
#     for user_id in users:
#         was_send = await safe_send_copy(user_id, from_chat, message)
#         if was_send:
#             send += 1
#         else:
#             not_send += 1
#     return send, not_send


async def safe_answer(event):
    try:
        await event.answer()
    except exceptions.TelegramBadRequest as e:
        if "query is too old" in str(e):
            pass
        else:
            logger.error(e)

    except Exception as e:
        logger.error(e)


async def safe_delete(event: Message | CallbackQuery):
    try:
        await event.message.delete()
    except exceptions.TelegramBadRequest as e:
        if "message to delete not found" in str(e):
            print(e)
            pass
        else:
            print(e)

    except Exception as e:
        print(e)

# async def send_by_instance(event: Message | CallbackQuery, text: str, reply_markup=None):
#     if isinstance(event, Message):
#         await event.answer(text, reply_markup=reply_markup)
#     else:
#         await safe_answer(event)
#         await safe_edit_text(event, text, reply_markup=reply_markup)
#
#
#
# async def get_and_clear(state: FSMContext):
#     try:
#         data = await state.get_data()
#         await state.clear()
#         return data
#     except Exception as e:
#         logger.error(e)
