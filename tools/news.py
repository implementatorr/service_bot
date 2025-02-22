import os
import logging
from dotenv import load_dotenv
from newsapi.newsapi_client import NewsApiClient
import random as rnd
from config.settings import SettingsManager
# Загрузка переменных окружения
load_dotenv()

# Настройка логирования для записи только ERROR и CRITICAL
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Инициализация NewsApiClient с ключом API
newsapi = NewsApiClient(api_key='fe2f50673b4d43b0a07fd93ce68708f8')

def get_world_news(topic, language='en'):
    """
    Функция для получения мировых новостей по заданной теме с ограничением по количеству статей.
    
    :param topic: Тема для поиска новостей.
    :param language: Язык новостей (по умолчанию английский).
    :return: Список статей.
    """
    try:
        # Логируем успешный запуск
        logger.info(f"Fetching news for topic: {topic} in {language} language.")
        
        # Получаем новости по теме с использованием get_top_headlines
        top_headlines = newsapi.get_top_headlines(category=topic, 
                                                  language=language)

        # Проверяем, есть ли данные в ответе
        if 'articles' not in top_headlines or not top_headlines['articles']:
            logger.warning(f"No articles found for the topic: {topic}")
            return []
        
        # Извлекаем статьи из ответа
        articles = top_headlines['articles']
        return articles
    
    except Exception as e:
        # Логируем ошибки
        logger.error(f"Error occurred while fetching news: {e}")
        return []


# Пример использования функции
def mainNewsapi():
    sm = SettingsManager()

    tags_list = []
    settings_topics = sm.get_setting('channel')[0]['tags']
    for tag in settings_topics:
        if tag['active'] == 1:  # Check if the tag is active
            tags_list.append(tag['tag'])
    topic = rnd.choice(tags_list)  # Тема для поиска 
    
    # Логируем начало получения новостей
    logger.info(f"Starting to fetch news on topic: {topic}")
    
    # Получаем новости
    news = get_world_news(topic)
    news_data = {}
    
    if news:
        for page, article in enumerate(news, 1):
            # Извлекаем данные статьи
            title = article.get('title')
            description = article.get('description')
            url = article.get('url')
            url_image = article.get('urlToImage')
            content = article.get('content')
            source = article.get('source')

            # Проверка данных
            if title and description and url and url_image and content and source:
                news_data[page] = {
                    'title': title,
                    'description': description,
                    'url': url,
                    'url_image': url_image,
                    'content': content,
                    'source': source 
                }
            else:
                logger.warning(f"Incomplete data for article {page}, skipping it.")
    else:
        logger.warning("No news found.")
    
    logger.info("News fetching complete.")
    return news_data

 

             


