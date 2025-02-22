from aiogram import BaseMiddleware
from aiogram.types import Update
import logging
from colorama import Fore, Style, init


# Настройка логирования
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# # Создание обработчика для вывода в консоль
# console_handler = logging.StreamHandler()


# # Настройка формата логов (добавляем время)
# formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", "%Y-%m-%d %H:%M:%S")
# console_handler.setFormatter(formatter)

# # Добавление обработчика к логгеру
# logger.addHandler(console_handler)


class LoggingMiddleware(BaseMiddleware):
    """
    Промежуточное ПО для логирования всех входящих обновлений (сообщений, callback-запросов и т.д.)
    и их содержимого.
    """

    async def __call__(self, handler, event, data: dict):
        """
        Обрабатывает обновление и логирует только необходимую информацию.
        """
        # Проверка, является ли событие обновлением сообщения
        
        if isinstance(event, Update):
            if event.message:
                # Если это сообщение, извлекаем его атрибуты
                update_id = event.message.message_id
                user_id = event.message.from_user.id
                user_name = event.message.from_user.username
                message_text = event.message.text

                # Логируем только необходимую информацию
                logger.info(Fore.GREEN + f"Message: user id={user_id} | @name='{user_name}' | text='{message_text}'")

            elif event.callback_query:
                # Если это callback-запрос, извлекаем его атрибуты
                update_id = event.callback_query.id
                user_id = event.callback_query.from_user.id
                user_name = event.callback_query.from_user.username
                callback_data = event.callback_query.data  # Данные, переданные с кнопкой

                # Логируем только необходимую информацию
                logger.info(Fore.YELLOW + f"CallbackQuery: user id={user_id} | @name='{user_name}' | callback='{callback_data}'")

        else:
            # Логируем тип обновления, если это не сообщение и не callback-запрос
            logger.info(f"Получено обновление типа {type(event)}")

        # Передаем обработчику (передаем событие и данные в следующий middleware или обработчик)
        return await handler(event, data)