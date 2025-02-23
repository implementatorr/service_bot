import asyncio
import logging
import random
from datetime import datetime, timezone
from aiogram import Bot
from tools.reqprocessing import mainproc
from chatgpt_md_converter import telegram_format as tf
from config.settings import SettingsManager

# Логирование
logger = logging.getLogger(__name__)



async def send_periodic_messages(bot: Bot):
    while True:
        try:
            # gettings settings
            sm = SettingsManager()
            flag: str = (sm.get_setting('settings.send')).lower()


            if flag != 'yes':  
                logger.info("Sending is disabled. Waiting for 5 minutes before retrying.")
                await asyncio.sleep(60 * 1)  
                continue  

            # quiet_hours
            quiet_hours = sm.get_setting('settings.quiet_hours')

            start = int(quiet_hours['start'])
            end = int(quiet_hours['end'])

            current_hour = datetime.now(timezone.utc).hour

            if (start <= current_hour < 24) or (0 <= current_hour < end):
                logger.info("It's night time (UTC). No messages will be sent.")
                await asyncio.sleep(3600)
                continue

            interval = int(sm.get_setting('settings.interval'))

            # get ads
            ads = sm.get_setting('settings.advertisement')

            ad_name = ads['name']
            ad_link = ads['url']

            channel_username = sm.get_setting('channel')[0]['id']

            # Получаем посты
            posts: dict = mainproc()

            if not posts:
                await asyncio.sleep(60)
                continue

            selected_post = random.choice(list(posts.items()))
            key, value = selected_post

            headline = value['content']
            description: str = value['description']
            url: str = value['url']
            url_image = value['url_image']
            source = value['source']['name']
            tags = value['tags']



            source_link = "http://" + url.split("//")[1].split("/")[0]
            tags_flag = sm.get_setting('settings.tags')
            if tags_flag.lower() == 'yes':
                tags = f'\n\n🔖 {tags}\n\n'
            else:
                tags = '\n\n'

            _description = tf(
                f'⚡️[**{headline}**]({url})\n\n'
                f'{description}...[**continue**]({url})'
                f'{tags}'
                f'▫️ **Source** : [**{source}**]({source_link})\n'
                f'▫️ **Our bot** : [**{ad_name}**]({ad_link})'
            )
            image_flag = sm.get_setting('settings.image')

            disable_preview_flag = sm.get_setting('settings.disable_web_page_preview')
            des_flag = True if disable_preview_flag.lower() == 'yes' else False
            
            if image_flag.lower() == 'yes':
                await bot.send_photo(
                    chat_id=channel_username, 
                    photo=url_image,
                    caption=_description,
                    parse_mode="HTML"
                )
            else:
                await bot.send_message(
                    chat_id=channel_username, 
                    text=_description,
                    parse_mode="HTML", 
                    disable_web_page_preview=des_flag
                )    

            random_delay = random.randint(interval - 5, interval + 5)
            logger.info(f"Message sent. Waiting for {random_delay * 60} minutes.")
            await asyncio.sleep(random_delay * 60)

        except Exception as e:
            logger.error(f"Error occurred while sending message: {e}")
            print(f"Ошибка: {e}")
            await asyncio.sleep(60)
