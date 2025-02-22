from aiogram.dispatcher.middlewares.base import BaseMiddleware
from config.settings import SettingsManager

class SMMiddleware(BaseMiddleware):
    def __init__(self, sm: SettingsManager):
        super().__init__()
        self.sm = sm

    async def __call__(self, handler, event, data):
        data["sm"] = self.sm
        return await handler(event, data)