import asyncio
from aiogram import Bot, Dispatcher
from app.handlers import router
from app.data_bot import bot_token

async def main():
    bot = Bot(token=bot_token)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
    except Exception:
        print("Произошла непредвиденная ошибка..")