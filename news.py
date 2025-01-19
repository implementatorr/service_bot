import os
import logging
from dotenv import load_dotenv
from newsapi.newsapi_client import NewsApiClient
import random as rnd
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
    topics = ['technology', 'science']
    topic = rnd.choice(topics)  # Тема для поиска 
    
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

 
#     x = {1: {'content': 'Team Asobi’s Astro Bot took the marquee Game of the Year '
#                 'prize at the 11th Game Awards, which were handed out Thursday '
#                 'at the Peacock Theater in Los Angeles. Astro Bot also '
#                 'garnered wins for Best Fam… [+3706 chars]',
#      'description': '2024 Game Awards announced their winners live on Thursday '
#                     'at Peacock Theater in Los Angeles',
#      'title': '2024 Game Awards Names ‘Astro Bot’ As Game Of The Year – '
#               'Complete Winners List - Deadline',
#      'url': 'http://deadline.com/2024/12/2024-game-awards-complete-winners-list-1236202365/',
#      'url_image': 'https://deadline.com/wp-content/uploads/2024/11/GameAwards2024.webp?w=1024'},
#  3: {'content': 'Onimusha is officially back. Capcom announced that the '
#                 'classic action series, which last received a proper sequel on '
#                 'the PlayStation 2, is getting a new entry on modern '
#                 'consoles.\r\n'
#                 'The first trailer w… [+1120 chars]',
#      'description': 'Onimusha is officially back. Capcom announced that the '
#                     'classic action series, which last received a proper '
#                     'sequel on the PlayStation 2, is getting a new entry on '
#                     'modern consoles.',
#      'title': 'Capcom Is Finally Bringing Back Onimusha - The Game Awards 2024 '
#               '- IGN',
#      'url': 'https://www.ign.com/articles/capcom-is-finally-bringing-back-onimusha-the-game-awards-2024',
#      'url_image': 'https://assets-prd.ignimgs.com/2024/12/13/onimusha-blogroll-1734057721384.jpg?width=1280'},
#  4: {'content': 'Helldivers 2 fans have been waiting patiently (and not so '
#                 'patiently) for the alien horde shooter to add a new enemy '
#                 'faction, and Arrowhead Studios is finally doing just that. '
#                 'The Illuminate are now l… [+1702 chars]',
#      'description': 'The Illuminate are back as the galactic war takes a '
#                     'frosty turn in Omens of Tyranny',
#      'title': 'Helldivers 2 Just Got Its Third Enemy Faction In A Major Free '
#               'Surprise Update - Kotaku',
#      'url': 'https://kotaku.com/helldivers-2-illuminate-omens-tyranny-free-update-1851720355',
#      'url_image': 'https://i.kinja-img.com/image/upload/c_fill,h_675,pg_1,q_80,w_1200/0d0b485623d76095b6db47fe6a99ea7f.jpg'},
#  6: {'content': 'FromSoftware is working on a new standalone game set in the '
#                 'world of Elden Ring.\r\n'
#                 "Revealed at tonight's The Game Awards, Elden Ring: Nightreign "
#                 'features plenty of familiar elements like sites of grac… '
#                 '[+2405 chars]',
#      'description': 'FromSoftware is working on a new standalone game set in '
#                     'the world of Elden Ring.',
#      'title': 'FromSoftware is making more Elden Ring after all, with the '
#               'co-op Elden Ring: Night Reign - Eurogamer',
#      'url': 'https://www.eurogamer.net/fromsoftware-is-making-more-elden-ring-after-all-with-the-co-op-elden-ring-night-reign',
#      'url_image': 'https://assetsio.gnwcdn.com/ELDEN-RING-NIGHTREIGN-%E2%80%93-REVEAL-GAMEPLAY-TRAILER-1-19-screenshot.png?width=1200&height=630&fit=crop&enable=upscale&auto=webp'},
#  8: {'content': 'Running a startup can be expensive, requiring a multitude of '
#                 'different subscriptions.\xa0Cap table management software, '
#                 'which helps founders organize their funding, can cost '
#                 'thousands of dollars a year.… [+4826 chars]',
#      'description': 'Cap table management firm Carta is under fire from some '
#                     'founders who say cancelling their subscriptions is too '
#                     'hard.',
#      'title': 'Carta is making it too difficult to cancel subscriptions, some '
#               'founders say - TechCrunch',
#      'url': 'https://techcrunch.com/2024/12/12/carta-is-making-it-too-difficult-to-cancel-subscriptions-some-founders-say/',
#      'url_image': 'https://techcrunch.com/wp-content/uploads/2018/12/Carta-Henry-Ward.jpg?resize=1200,800'},
#  10: {'content': 'NurPhoto / Contributor / Getty Images\r\n'
#                  'With the holiday season upon us, many companies are finding '
#                  'ways to take advantage through deals, promotions, or other '
#                  'campaigns. OpenAI has found a way to part… [+9512 chars]',
#       'description': 'For 12 days, the OpenAI daily live stream is unveiling '
#                      "'new things, big and small.' Here's what's new today.",
#       'title': "ChatGPT's Advanced Voice Mode finally gets visual context on "
#                'the 6th day of OpenAI - ZDNet',
#       'url': 'https://www.zdnet.com/article/chatgpts-advanced-voice-mode-finally-gets-visual-context-on-the-6th-day-of-openai/',
#       'url_image': 'https://www.zdnet.com/a/img/resize/1259dd9b89e5903b23ac61aabadbae89f83666e0/2024/12/10/69b859a7-b629-4e34-a869-486c4cb85247/gettyimages-2187409024.jpg?auto=webp&fit=crop&height=675&width=1200'},  
#  11: {'content': 'Gemini AI can now summarize whats in your Google Drive '
#                  'folders\r\n'
#                  'Gemini AI can now summarize whats in your Google Drive '
#                  'folders\r\n'
#                  ' / You can get a glimpse at the contents of a folder without '
#                  'having to … [+1345 chars]',
#       'description': 'Google Gemini can now summarize the contents of your '
#                      'folder, allowing you to get a glimpse at what’s in your '
#                      'folder without having to dig through it.',
#       'title': 'Gemini AI can now summarize what’s in your Google Drive '
#                'folders - The Verge',
#       'url': 'https://www.theverge.com/2024/12/12/24319697/gemini-ai-summarize-google-drive-folders',
#       'url_image': 'https://cdn.vox-cdn.com/thumbor/myFkNONhMBCxfmB3njKKDC7KF2U=/0x0:3000x2000/1200x628/filters:focal(1500x1000:1501x1001)/cdn.vox-cdn.com/uploads/chorus_asset/file/23954498/acastro_STK459_02.jpg'},  
#  12: {'content': 'Mariner, the ew AI agent from Google, leverages the Gemini '
#                  '2.0 platform\r\n'
#                  'NurPhoto via Getty Images\r\n'
#                  'Google has introduced Mariner, an advanced AI agent and '
#                  'prototype powered by its Gemini 2.0 framewo… [+4783 chars]',
#       'description': 'Google has introduced Mariner, an advanced AI agent and '
#                      "prototype powered by its Gemini 2.0 framework. Here's "
#                      'how the AI agent is changing the search game online.',
#       'title': 'Google Launches Mariner, A New AI Agent Based On Updated '
#                'Gemini 2.0 - Forbes',
#       'url': 'https://www.forbes.com/sites/chriswestfall/2024/12/12/google-launches-mariner-a-new-ai-agent-based-on-updated-gemini-20/',
#       'url_image': 'https://imageio.forbes.com/specials-images/imageserve/675b0d55ed3ac1fe3cf98c49/0x0.jpg?format=jpg&crop=2126,1195,x0,y109,safe&height=900&width=1600&fit=bounds'},
#  13: {'content': 'The Android operating system runs on billions of devices '
#                  'worldwide. Most of them are phones, but many of them are '
#                  'also tablets, smartwatches, televisions, cars, and a bunch '
#                  'of random IoT products. Of… [+11059 chars]',
#       'description': 'Google Glass and Daydream VR nod in approval',
#       'title': 'Google wants Android XR to power your next VR headset and '
#                'smart glasses - Android Police',
#       'url': 'https://www.androidpolice.com/android-xr-announced/',
#       'url_image': 'https://static1.anpoimages.com/wordpress/wp-content/uploads/2024/12/google-wants-android-xr-to-power-your-next-vr-headset.jpg'},
#  14: {'content': 'With iOS 18.2, Apple completes its AI starter kit\r\n'
#                  'With iOS 18.2, Apple completes its AI starter kit\r\n'
#                  ' / Rewrite your emails like Shakespeare? Weird image '
#                  'generator? Brainstorm dinner recipes with a … [+6291 chars]',
#       'description': 'Apple Intelligence gets its second major update with iOS '
#                      '18.2, but the AI feature set feels very familiar.',
#       'title': 'With iOS 18.2, Apple completes its AI starter kit - The Verge',
#       'url': 'https://www.theverge.com/2024/12/12/24318840/ios-18-2-apple-intelligence-chatgpt-genmoji-image-playground',
#       'url_image': 'https://cdn.vox-cdn.com/thumbor/Ow-Z73uBpUorQWnfntD_pOXkKoA=/0x0:2000x1333/1200x628/filters:focal(1000x667:1001x668)/cdn.vox-cdn.com/uploads/chorus_asset/file/25786197/DSC08569_processed.jpg'}}
#     # Печать первой статьи
             


