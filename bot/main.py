from aiogram import Bot
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from config import WEBAPP_HOST, WEBAPP_PORT, WEBHOOK_PATH, WEBHOOK_URL
from create import bot, dp
from handlers import router

app = web.Application()


async def on_startup(bot: Bot):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)

def main():
    dp.include_routers(
        router
    )

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)

    dp.startup.register(on_startup)

    setup_application(app, dp, bot=bot)
    web.run_app(app, host=WEBAPP_HOST, port=int(WEBAPP_PORT))


if __name__ == "__main__":
    main()
