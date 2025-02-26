import logging
from collections import deque
from tools.gpt import mainGptAPI
from tools.news import mainNewsapi
from config.settings import SettingsManager
import random
from pprint import pprint

# Set up logging to show only ERROR and WARNING
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Ограниченная очередь на 5 элементов
headline_useed = deque(maxlen=100)

def requestprocessing(news: dict, language='en'):
    global headline_useed
    translation_lang = {
        "de": "german",
        "ru": "russian",
        "pt": "portuguese",
        "de": "german"
    }
    language = translation_lang.get(language)

    # Создание строки для передачи в GPT
    
    # Получаем настройки
    sm = SettingsManager()
    headline = sm.get_setting("settings.headline")

    #random text length
    text_length = sm.get_setting('settings.message_length')
    text_length = text_length.split("-")
    text_length = random.randint(int(text_length[0]), int(text_length[1]))

    hashtags = sm.get_setting('settings')['hashtags_count']

    news_data = ""
    try:
        for article_id, article in news.items():

            #проверем отпрален ли пост уже или нет
            if article['url_image'] not in headline_useed:            
                description = article['description']
                news_data += f"{article_id} : {description}" 
    except Exception as e:
        logger.error(f"Error processing news data: {e}")     
    
    # Получаем 3 самых интересных новости
    try:
        gpt_response: str = mainGptAPI(
            text=news_data,
            prompt="Please return only the number of the most interesting news article about AI and technology, gaming."
                f"Format the response as 1 or 2 or 11 etc. without any additional text or details."
        )
        logger.info(f"GPT API response: {gpt_response}")
    except Exception as e:
        logger.error(f"Error during GPT API call: {e}")
        return {}

    # Преобразуем ответ GPT в список чисел
    try:
        gpt_response_list = [int(num.strip()) for num in gpt_response.split(",") if num.strip().isdigit()]
        logger.info(f"Extracted article IDs: {gpt_response_list}")
    except ValueError as e:
        logger.error(f"Error processing GPT response: {e}")
        return {}

    try:
        response = {}
        for key, value in news.items():
            if key in gpt_response_list:
                response[key] = value
        logger.info(f"Selected articles: {response}")        
    except Exception as e:
        logger.error(f"Error processing news data: {e}")
        return {}            


    # Создание заголовков и обновление headline_useed
    for key, value in response.items():
        try:
            value['content'] = mainGptAPI(
                text=value['content'],
                prompt=f"Make it a {headline} word headline. Return only the reformatted text."
                        f"Use {language} language from the provided content."
            )
            # logger.info(f"Headline created: {value['content']}")
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
                       f"Use {language} language from the provided content."
            )
            # logger.info(f"News text created: {value['description']}")
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
                       f"Use {language} language from the provided content."
            )
            # logger.info(f"Tags created: {value['tags']}")
        except Exception as e:
            logger.error(f"Error processing content for tags {key}: {e}")
            value['tags'] = "Error occurred while processing tags."

    try:
        url_image = response[gpt_response_list[0]]['url_image']
        headline_useed.append(url_image)
    except Exception as e:
        logger.error(f"Error adding image URL: {e}")
    return response

def mainproc(language='en'):
    try:
        news = mainNewsapi(language=language)
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        return {}
    
    logger.info(f"Starting processing of {len(news)} news articles with ChatGPT.")
    return requestprocessing(news=news, language=language)
