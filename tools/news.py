import os
import logging
from dotenv import load_dotenv
from newsapi.newsapi_client import NewsApiClient
import random as rnd
from config.settings import tech_terms
from pprint import pprint
from datetime import datetime, timedelta
import random
# Загрузка переменных окружения
load_dotenv()

# Настройка логирования для записи только ERROR и CRITICAL
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


def get_world_news(language='en'):
    """
    Функция для получения мировых новостей по заданной теме с ограничением по количеству статей.
    
    :param language: Язык новостей (по умолчанию английский).
    :return: Список статей.
    """
    try:
        date_one_day_ago = (datetime.now() - timedelta(days=4)).strftime("%Y-%m-%d")
        lang_texch = tech_terms.get(language)
        print(lang_texch)

        while True:
            random_token = random.choice(['NEWS_API2', 'NEWS_API3'])

            # Инициализация NewsApiClient с ключом API
            TOKEN = os.getenv(random_token)
            print(TOKEN)
            newsapi = NewsApiClient(api_key=TOKEN)
            topic = random.choice(lang_texch)  # Use random.choice instead of rnd.choice

            # Логируем успешный запуск
            logger.info(f"Fetching news for topic: {topic} in {language} language.")
            
            # Получаем новости по теме с использованием get_everything
            news_data = newsapi.get_everything(
                q=topic,  # Ключевые слова или фраза для поиска как в заголовке, так и в теле статьи.
                language=language,  # Двухбуквенный код языка для поиска новостей
                from_param=date_one_day_ago,  # Дата и время, начиная с которых будут искаться статьи.
                page_size=70,
                sort_by='popularity'  # Количество статей, которые нужно вернуть на одну страницу. Максимум — 100.
            )
            
            if len(news_data['articles']) > 5 and news_data['status'] == 'ok':
                break
            else:
                logger.warning(f"No articles found for the topic: {topic}, len: {len(news_data['articles'])}")

        logger.info(f"Successfully fetched news for topic: {topic} in {language} language.")    
        return news_data['articles']
    
    except Exception as e:
        logger.error(f"Error occurred while fetching news: {e}")
        return []


# Пример использования функции
def mainNewsapi(language='en'):
    logger.info(f"Starting to fetch news wthi language: {language}.")
    
    # Получаем новости
    news = get_world_news(language)
    news_data = {}
    if news:
        # Обрабатываем каждую статью
        for page, article in enumerate(news, 1):

            if isinstance(article, dict):
                # Извлекаем данные статьи
                title = article.get('title')
                description = article.get('description')
                url = article.get('url')
                url_image = article.get('urlToImage')
                content = article.get('content')
                source = article.get('source', {}).get('name')

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
        logger.warning(f"No news found, language: {language}.")
    
    logger.info(f"News fetching complete, language: {language}.")
    return news_data







# if __name__ == "__main__":
#     news = mainNewsapi(language='de')
#     print(len(news))   

             


