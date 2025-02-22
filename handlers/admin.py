from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputFile, FSInputFile, InputMediaPhoto
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from chatgpt_md_converter import telegram_format as tf
from keyboard.inline import tag_kb, universal_kb
from config.settings import SettingsManager, settings_dict
from aiogram import Bot
from datetime import datetime, timezone

admin_router = Router()

class AdminState(StatesGroup):
    wait_request_item = State()
    wait_post = State()
    post_info = State()
    wait_admin_id = State()
    wait_change_channel = State()



def get_settings_text(sm: SettingsManager):
    current_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    settings = sm.get_setting('settings')
    text = tf(
        f"**Time UTC now: {current_time}**\n\n"
        f"`**Headline length:**`  **{settings['headline']}** word(s)\n"
        f"`**Message length:**`  **{settings['message_length']}** word(s)\n"
        f"`**Number of hashtags:**` {settings['hashtags_count']}\n"
        f"\n`**Interval:**` {settings['interval']} min\n"
        f"\n`**Quiet hours:**`\n"
        f"  - `**Quiet hours start:**` {settings['quiet_hours']['start']} utc\n"
        f"  - `**Quiet hours end:**` {settings['quiet_hours']['end']} utc \n"
        f"\n`**Advertisement:**`\n"
        f"  - `**Name:**` {settings['advertisement']['name']}\n"
        f"  - `**URL:**` {settings['advertisement']['url']}\n\n"
        f"`**Send:**` {'✅' if settings['send'].lower() == 'yes' else '❌'}\n"
        f"`**Tags:**` {'✅' if settings['tags'].lower() == 'yes' else '❌'}\n"
        f"`**Image:**` {'✅' if settings['image'].lower() == 'yes' else '❌'}\n\n"
        f"`**Disable preview:**` {'✅' if settings['image'].lower() == 'yes' else '❌'}\n\n"
        f"`**Admin:**` {settings['admin']}\n"
    )
    return text

async def admin_main(message: Message, state: FSMContext):
    await state.clear()
    buttons = [
        "🔄Change Channel",
        "🚩Send Post",
        "🔧Settings"
    ]
    try:
        await message.edit_text(
            text=tf('**Admin panel**'),
            reply_markup=universal_kb(buttons))
    except:
        await message.answer(
            text=tf('**Admin panel**'),
            reply_markup=universal_kb(buttons))  

@admin_router.message(Command(commands=['admin']))
async def handle_account_command(message: Message, state: FSMContext) -> None:
    await admin_main(message, state)
    

@admin_router.callback_query(F.data == '🔧Settings')
async def proccess_requests(callback: CallbackQuery, sm: SettingsManager, state: FSMContext):
    text = get_settings_text(sm)
    await state.set_state(AdminState.wait_request_item)
    await callback.message.edit_text(text, reply_markup=universal_kb(['Back Main'], 'back_main'))


@admin_router.message(AdminState.wait_request_item)
async def change_requests(message: Message, state: FSMContext, sm: SettingsManager):
    for key, value in settings_dict.items():
        if key in message.text:
            settings_value = value
            amount = message.text.replace(f"{key}:", '').strip()
    try:
        sm.update_setting(key=settings_value, value=amount)        
        text = get_settings_text(sm)
        await message.answer(text, reply_markup=universal_kb(['Back Main'], 'back_main'))
    except:
        await message.answer(text='Try one more time', reply_markup=universal_kb(['Back Main'], 'back_main'))    


@admin_router.callback_query(F.data == 'back_main_Back Main')
async def back_main(callback: CallbackQuery, state: FSMContext):
    await admin_main(callback.message, state)


@admin_router.callback_query(F.data == '🚩Send Post')
async def proccess_send_post(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AdminState.wait_post)
    text = "Write a post you want to make, with or without a photo - >>>"
    await callback.message.edit_text(text, reply_markup=universal_kb(['Back Main'], 'back_main')) 


@admin_router.message(AdminState.wait_post)
async def process_post(message: Message, state: FSMContext):
    user_id = message.from_user.id
    photo_path = None  # Изначально фото не задано
    buttons = ['Send Post', 'Send/Pin Post']
    # Проверяем, есть ли фото
    if message.photo:
        # Получаем ID файла
        file_id = message.photo[-1].file_id
        # Получаем объект файла через bot.get_file()
        file = await message.bot.get_file(file_id)
        # Скачиваем файл
        photo_path = f"images/{user_id}_photo.jpg"
        await message.bot.download_file(file.file_path, photo_path)

        # Текст из подписи
        text = message.caption if message.caption else "No caption provided"
        image_path = photo_path
        image = FSInputFile(image_path)
        await message.answer_photo(photo=image, caption=text, reply_markup=universal_kb(buttons))
    else:
        # Если фото нет, сохраняем только текст
        text = message.text
        await message.answer(f"Post saved without photo. Text: {text}", reply_markup=universal_kb(buttons))

    await state.update_data(post_info = [photo_path, text])


    

@admin_router.callback_query(F.data == 'Send Post' or F.data == 'Send/Pin Post')
async def process_send_post(callback: CallbackQuery, state: FSMContext, bot: Bot, sm: SettingsManager):
    # Получаем сохранённые данные о посте из состояния
    user_data = await state.get_data()
    photo_path, text = user_data.get('post_info', (None, None))
    channel_id = sm.get_setting('channel')[0]['id']
    pin = True if callback.data == 'Send/Pin Post' else False

    if photo_path:
        image_path = photo_path
        image = FSInputFile(image_path)
        sent_message = await bot.send_photo(
            chat_id=channel_id,
            photo=image,
            caption=text
        )
        
        await callback.message.answer_photo(photo=image, caption=tf(f"**Message has been sent**:\n\n{text}"))
    else:
        # Если фото нет, просто отправляем текст
        sent_message = await bot.send_message(chat_id=channel_id, text=tf(text))
        await callback.message.answer(tf(f"**Message has been sent**:\n\n{text}")) 

    if pin:
        await bot.pin_chat_message(
                chat_id=channel_id,  # ID канала или чата
                message_id=sent_message.message_id  # ID отправленного сообщения
            )
        await callback.message.answer(text=tf("Message is pinned"))    

#chanel info
async def channel_change_info(callback: CallbackQuery,  bot: Bot, sm: SettingsManager):
    #getting tags  
    channel_settings = sm.get_setting('channel')[0]
    channel_tags = channel_settings['tags']

    #getting_channel info
    channel_name = sm.get_setting('channel')[0]['id']
    chat_info = await bot.get_chat(channel_name)

    chat_id = chat_info.id
    title = chat_info.title
    members_count = await bot.get_chat_member_count(chat_id)
    channel_type = chat_info.type
    admins = await bot.get_chat_administrators(chat_id)

    admins_list = "\n".join([f" -  @{admin.user.username} - {admin.status}" for admin in admins])

    text = tf(
        f"**Channel:** @{title}\n"
        f"**ID:** {chat_id}\n"
        f"**Members Count:** {members_count}\n"
        f"**Channel Type:** {channel_type}\n\n"
        f"**Admins:**\n{admins_list if admins else 'No admins available'}\n\n"
        f"Language: {channel_settings['language']}\n"
    )
    await callback.message.edit_text(text, reply_markup=tag_kb(channel_tags, 'tags')) 



@admin_router.callback_query(F.data == "🔄Change Channel")
async def change_channel(callback: CallbackQuery,  bot: Bot, sm: SettingsManager):     
    await channel_change_info(callback, bot, sm) 

@admin_router.callback_query(F.data.startswith('tags'))    
async def proccess_tags(callback: CallbackQuery, sm: SettingsManager, bot: Bot):
    tag = callback.data.replace('tags_', '')
    tag_status = sm.get_setting('channel')[0]['tags']
    for status in tag_status:
        if status['tag'] == tag:
            active = status['active']
    sm.update_tag_activation(tag, 0 if active == 1 else 1)
    await channel_change_info(callback, bot, sm) 
        
