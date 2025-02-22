from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def universal_kb(buttons: list, callback: str =  None) -> InlineKeyboardMarkup:
    row = []
    for button_name in buttons:
        if callback:
            call_data = f"{callback}_{button_name}"
        else:
            call_data = f"{button_name}"
        row.append([InlineKeyboardButton(text=button_name, callback_data=call_data)])
    
    return InlineKeyboardMarkup(inline_keyboard=row)  # Оборачиваем row в список


def tag_kb(tags: list, callback: str = None) -> InlineKeyboardMarkup:
    row = []
    for tag in tags:
        if callback:
            call_data = f"{callback}_{tag['tag']}"
        else:
            call_data = f"{tag['tag']}"
        
        # Check if the tag is active or inactive and create the appropriate label
        button_flag = f'✅ {tag["tag"]}' if tag['active'] == 1 else f'❌ {tag["tag"]}'
        
        # Add button to the row
        row.append([InlineKeyboardButton(text=button_flag, callback_data=call_data)])

    row.append([InlineKeyboardButton(text='<- Back Main', callback_data='back_main_Back Main')])
    return InlineKeyboardMarkup(inline_keyboard=row)

