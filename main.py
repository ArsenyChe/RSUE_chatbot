import asyncio
from os import getenv
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from callbacks import evaluationg_message
from handlers import commands, responses

async def main():
    load_dotenv()
    bot = Bot(getenv('TOKEN_API'))

    dp = Dispatcher()
    dp.include_routers(commands.router,
                       evaluationg_message.router,
                       responses.router)
    print(f'[INFO] Bot connect')

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e: 
        print(f'[INFO] Bot run {e}')