from aiogram.dispatcher.middlewares.base import BaseMiddleware
import os
from aiogram.types import Message, CallbackQuery
from dotenv import load_dotenv
from config.settings import SettingsManager

load_dotenv()

# Получаем ADMIN_ID из переменных окружения и преобразуем его в список
ADMIN_ID = os.getenv('ADMIN')



class AdminMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()
        self.admins = [ADMIN_ID]

    async def __call__(self, handler, event, data):
        sm = SettingsManager()
        new_admin = sm.get_setting('settings.admin')
        self.admins = [ADMIN_ID, new_admin]
        
        if event.message is None:
            user_id = str(event.callback_query.from_user.id)
        else:    
            user_id = str(event.message.from_user.id)
        
        if user_id not in self.admins:
            return  # Если не админ, просто выходим

        return await handler(event, data)  # Передаем управление дальше

        
