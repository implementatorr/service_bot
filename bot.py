import asyncio
import logging
import os
import ssl
from dotenv import load_dotenv
from colorama import Fore, Style
from aiogram import Bot, Dispatcher, types
from broadcast.channel_sender import send_periodic_messages
from middleware.setmidware import SMMiddleware
from middleware.adminmidware import AdminMiddleware
from middleware.loggingmidware import LoggingMiddleware
from handlers.admin import admin_router  # Импортируем функцию отправки сообщений
from config.settings import SettingsManager
from cmd.commands import private_commands
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode 
# from telethon import TelegramClient


load_dotenv()

TOKEN = os.getenv('TELEGRAM_API_TOKEN')
# api_id = os.getenv('API_ID')
# api_hash = os.getenv("API_HASH")

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
# client = TelegramClient('session_name', api_id, api_hash)

# Setup logger
logger = logging.getLogger()


async def main() -> None:
    
    # await client.start()
    # me = await client.get_me()
    
    dp = Dispatcher()
    sm = SettingsManager()
    dp.include_router(admin_router)

    dp.update.middleware(SMMiddleware(sm))
    dp.update.middleware(AdminMiddleware())
    dp.update.middleware(LoggingMiddleware())

    await bot.set_my_commands(
        commands=private_commands, scope=types.BotCommandScopeAllPrivateChats()
    )

    # await get_last_message(client=client)

    await asyncio.gather(
        dp.start_polling(bot),
        send_periodic_messages(bot),  # Запуск функции отправки сообщений   
    )
    # await client.disconnect()

if __name__ == "__main__":
    try:
        logger.info(Fore.GREEN + "Bot started." + Style.RESET_ALL)
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info(Fore.RED + "Bot stopped by user." + Style.RESET_ALL)
    except Exception as e:
        logger.error(Fore.RED + f"An error occurred: {e}" + Style.RESET_ALL)
    finally:
        pass # Логируем отключение клиента
