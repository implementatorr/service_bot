import json
import os

class SettingsManager:
    def __init__(self, filename='settings.json'):
        self.current_dir = os.path.dirname(__file__)
        self.file_path = os.path.join(self.current_dir, filename)
        self.settings = self.load_settings()

    def load_settings(self):
        """Загружает настройки из JSON-файла."""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Файл {self.file_path} не найден.")
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def save_settings(self):
        """Сохраняет текущие настройки в JSON-файл."""
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(self.settings, file, ensure_ascii=False, indent=4)

    def update_setting(self, key, value):
        """Обновляет определённый параметр и сохраняет изменения."""
        keys = key.split(".")
        target = self.settings

        for k in keys[:-1]:
            if k in target:
                target = target[k]
            else:
                raise KeyError(f"Ключ {key} не найден в настройках.")

        if keys[-1] in target:
            target[keys[-1]] = value
            self.save_settings()
        else:
            raise KeyError(f"Ключ {key} не найден в настройках.")
        
    def update_tag_activation(self, tag_name, new_status):
        """Обновляет статус активности тега."""
        try:
            # Loop through each channel
            for channel in self.settings["channel"]:
                # Loop through each tag in the channel
                for tag in channel["tags"]:
                    if tag["tag"] == tag_name:
                        tag["active"] = new_status  # Set new status (1 or 0)
                        self.save_settings()  # Save updated settings
                        print(f"Tag {tag_name} activation updated to {new_status}.")
                        return
            raise KeyError(f"Tag {tag_name} not found.")
        except KeyError as e:
            print(e)

    def get_setting(self, key):
        """Получает значение определённого параметра."""
        keys = key.split(".")
        target = self.settings

        for k in keys:
            if k in target:
                target = target[k]
            else:
                raise KeyError(f"Ключ {key} не найден в настройках.")
        return target

    def get_channels(self):
        """Возвращает список каналов."""
        return self.settings.get("channels", [])

    def get_channel_by_id(self, channel_id):
        """Возвращает параметры канала по его ID."""
        for channel in self.settings.get("channels", []):
            if channel["id"] == channel_id:
                return channel
        return None

    def set_channel_status(self, channel_id, status):
        """Изменяет параметр 'send' (true/false) для указанного канала."""
        for channel in self.settings.get("channels", []):
            if channel["id"] == channel_id:
                channel["send"] = status
                self.save_settings()
                return True
        return False

settings_dict = {
    "Message length": "settings.message_length",
    "Number of hashtags": "settings.hashtags_count",
    "Interval": "settings.interval",
    "Admin": "settings.admin",
    "Send": "settings.send",
    "Name": "settings.advertisement.name",
    "URL": "settings.advertisement.url",
    "Quiet hours start": "settings.quiet_hours.start",  
    "Quiet hours end": "settings.quiet_hours.end",      
    "Headline length": "settings.headline",
    "Tags": "settings.tags",
    "Image": "settings.image",        
}


# if __name__=='__main__':
#     sm = SettingsManager()
#     # headline = sm.get_setting("settings.headline")
#     # text_length = sm.get_setting('settings.message_length')
#     # hashtags = sm.get_setting('settings.hashtags_count')
#     tags_list = []
#     settings_topics = sm.get_setting('channel')[0]['tags']
#     for tag in settings_topics:
#         if tag['active'] == 1:  # Check if the tag is active
#             tags_list.append(tag['tag'])  # Add the tag to the list if active

#     print(tags_list)          




# # Импортируем класс
# from settings_manager import SettingsManager

# # Создаём экземпляр менеджера настроек
# manager = SettingsManager()

# # 1. Получение параметров
# print("Длина сообщения:", manager.get_setting("settings.message_length"))
# print("Количество хэштегов:", manager.get_setting("settings.hashtags_count"))

# # 2. Изменение параметра и сохранение
# manager.update_setting("settings.message_length", 600)
# print("Новая длина сообщения:", manager.get_setting("settings.message_length"))

# # 3. Получение списка всех каналов
# channels = manager.get_channels()
# print("Каналы:", channels)

# # 4. Получение информации о конкретном канале
# channel_info = manager.get_channel_by_id("CHANNEL_ID_1")
# if channel_info:
#     print("Информация о канале:", channel_info)
# else:
#     print("Канал не найден")

# # 5. Изменение статуса отправки сообщений в канале
# success = manager.set_channel_status("CHANNEL_ID_1", False)
# if success:
#     print("Статус канала обновлён")
# else:
#     print("Канал не найден")

# # 6. Изменение рекламного блока
# manager.update_setting("settings.advertisement.name", "New Sponsor")
# manager.update_setting("settings.advertisement.url", "https://example.com")

# # 7. Проверка изменений
# print("Обновлённая реклама:", manager.get_setting("settings.advertisement"))