import logging
from collections import deque
from tools.gpt import mainGptAPI
from tools.news import mainNewsapi
from config.settings import SettingsManager

# Set up logging to show only ERROR and WARNING
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Ограниченная очередь на 5 элементов
headline_useed = deque(maxlen=5)

def requestprocessing(news: dict):
    global headline_useed

    # Создание строки для передачи в GPT
    headline_str = ", ".join(map(str, headline_useed))
    print(headline_str)
    # Получаем настройки
    sm = SettingsManager()
    headline = sm.get_setting("settings.headline")
    text_length = sm.get_setting('settings.message_length')
    hashtags = sm.get_setting('settings')['hashtags_count']

    news_data = ""

    for article_id, article in news.items():
        
        description = article['description']
        news_data += f"{article_id} : {description} "       
    
    # Получаем 3 самых интересных новости
    try:
        gpt_response: str = mainGptAPI(
            text=news_data,
            prompt=f"Please return only the numbers of the 3 most interesting news articles about AI and technology. "
                f"Do NOT include information related to the following themes: {headline_str}. "
                f"Format the response as 1, 2, 3, etc. without any additional text or details."
        )
    except Exception as e:
        logger.error(f"Error during GPT API call: {e}")
        return {}

    # Преобразуем ответ GPT в список чисел
    try:
        gpt_response_list = [int(num.strip()) for num in gpt_response.split(",") if num.strip().isdigit()]
    except ValueError as e:
        logger.error(f"Error processing GPT response: {e}")
        return {}

    response = {}
    for key, value in news.items():
        if key in gpt_response_list:
            response[key] = value

    # Создание заголовков и обновление headline_useed
    for key, value in response.items():
        try:
            value['content'] = mainGptAPI(
                text=value['content'],
                prompt=f"Make it a {headline} word headline. Return only the reformatted text."
            )
            headline_useed.append(value['content'])  # Добавляем новый заголовок
        except Exception as e:
            logger.error(f"Error processing content for article {key}: {e}")
            value['content'] = "Error occurred while processing content."

    # Создание новостного текста
    for key, value in response.items():
        try:
            value['description'] = mainGptAPI(
                text=f"{value['description']}, {value['content']}",
                prompt=f"Create a {text_length} simple word news-style text based on the provided information. "
                       f"Keep it concise, engaging, and clear for a general audience. "
                       f"Focus on the key details and make it easy to read. Return only the result."
            )
        except Exception as e:
            logger.error(f"Error processing content for description {key}: {e}")
            value['description'] = "Error occurred while processing content."

    # Создание хэштегов
    for key, value in response.items():
        try:
            value['tags'] = mainGptAPI(
                text=f"{value['description']}, {value['content']}",
                prompt=f"Generate {hashtags} popular and relevant hashtags based on the provided text. "
                       f"Focus on the main topics and trends related to the content. Return only the result."
            )
        except Exception as e:
            logger.error(f"Error processing content for tags {key}: {e}")
            value['tags'] = "Error occurred while processing tags."

    return response

def mainproc():
    try:
        news = mainNewsapi()
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        return {}

    return requestprocessing(news=news)
