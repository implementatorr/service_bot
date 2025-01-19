import logging
import requests
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования для отображения только ошибок и критических ошибок
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Функция для получения ответа от модели GPT-4
def get_gpt4_response(prompt: str, text: str, api_key: str) -> str:
    url = "https://api.openai.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "gpt-4o-mini",  # Используем правильную модель
        "temperature": 0.7,
        "max_tokens": 150,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text},
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        # Отправка POST запроса к API
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Это автоматически выбросит исключение при ошибке ответа
        result = response.json()
        return result['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        # Логируем ошибки с уровнями ERROR или CRITICAL
        logger.error(f"Request failed: {str(e)}")
        print(f"Request failed: {str(e)}")
        return f"Error: {str(e)}"

# Пример использования функции
def mainGptAPI(text: str = None, prompt: str = None):
    # API ключ OpenAI
    api_key = os.getenv('OPENAI_API_KEY')  # Замените на свой API-ключ
    # print(api_key)
    # Получаем ответ от GPT-4
    response = get_gpt4_response(prompt, text, api_key)
    return response
