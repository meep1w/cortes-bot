from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import asyncio
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    @dp.message(CommandStart())
    async def start(message: types.Message):
        await message.answer("✅ Бот работает! /start получен.")

    @dp.message()
    async def echo(message: types.Message):
        await message.answer("Ты написал: " + message.text)

    print("✅ Бот запущен. Ждём сообщения...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
