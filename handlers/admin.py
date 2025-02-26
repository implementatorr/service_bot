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


