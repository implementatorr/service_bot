import asyncio
import logging
import os
from dotenv import load_dotenv
from colorama import Fore, Style
from chatgpt_md_converter import telegram_format as tf
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.dispatcher.router import Router
from aiogram.filters import Command
from reqprocessing import mainproc
import random
from datetime import datetime, timezone
load_dotenv()

TOKEN = os.getenv('TELEGRAM_API_TOKEN')
GROUP_CHAT_ID = os.getenv('GROUP_CHAT_ID')  # Идентификатор группы, где бот администратор
bot = Bot(token=TOKEN)  # Используйте parse_mode вместо default

# Setup logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger('aiogram').setLevel(logging.INFO)
# Инициализация Router
router = Router()

# Пример обработчика для команды /start
@router.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Я бот!")

# Функция для отправки сообщений в группу каждые 10 секунд
async def send_periodic_messages():
    while True:
        try:
            # Проверка текущего времени (UTC)
            current_hour = datetime.now(timezone.utc).hour
            if 23 <= current_hour < 7:
                # Если текущее время с 23:00 до 7:00 (UTC), пропускаем отправку
                logger.info("It's night time (UTC). No messages will be sent.")
                await asyncio.sleep(3600)  # Ожидаем 1 час и проверяем снова
                continue
            
            chat_id = GROUP_CHAT_ID
            posts: dict = mainproc()
            # Выбираем случайную новость из списка
            selected_post = random.choice(list(posts.items()))
            key, value = selected_post
            headline = value['content']
            description: str = value['description']
            title = value['title']
            url: str = value['url']
            url_image = value['url_image']
            source = value['source']['name']
            tags = value['tags']


            source_link = url.split("//")[1]
            source_link = source_link.split("/")[0]
            finall_source_link = "http://" + source_link

            bot_link = "https://t.me/Gpt_modeBot"

            _description = tf(
                f'[**{headline}**]({url})\n\n'
                f'{description}...[**continue**]({url})\n\n'
                f'{tags}\n\n'
                f'**Source** : [{source}]({finall_source_link})\n'
                f'**Our bot** : [ChatGPT Bot]({bot_link})'       
            )

            # Отправка сообщения в группу
            await bot.send_photo(
                chat_id=chat_id, 
                photo=url_image,
                caption=_description,
                parse_mode="HTML"
            )

            # Случайная задержка от 55 до 65 минут
            random_delay = random.randint(55 * 60, 65 * 60)  # В секундах
            logger.info(f"Message sent. Waiting for {random_delay / 60:.2f} minutes.")
            await asyncio.sleep(random_delay)

        except Exception as e:
            logger.error(f"Error occurred while sending message: {e}")
            await asyncio.sleep(60)  # Если произошла ошибка, пробуем снова через минуту


async def main() -> None:
    """
    Initialize and start the bot.
    """
    dp = Dispatcher()

    # Регистрируем роутеры (если они есть)
    dp.include_router(router)

    # Запускаем бота с polling
    await asyncio.gather(
        dp.start_polling(bot),
        send_periodic_messages()  # Запускаем функцию для отправки сообщений каждые 10 секунд
    )

if __name__ == "__main__":
    try:
        logger.info(Fore.GREEN + "Bot started." + Style.RESET_ALL)
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info(Fore.RED + "Bot stopped by user." + Style.RESET_ALL)
    except Exception as e:
        logger.error(Fore.RED + f"An error occurred: {e}" + Style.RESET_ALL)
