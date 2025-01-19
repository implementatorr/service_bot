import logging
from gpt import mainGptAPI
from news import mainNewsapi

# Set up logging to show only ERROR and WARNING
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def requestprocessing(news: dict):
    for_gpt_request: str = ""

    try:
        gpt_response: str = mainGptAPI(
            text=for_gpt_request,
            prompt="Please return only the numbers of the 3 most interesting news articles about AI and technology in the format 1, 2, 3, etc. Do not include any additional text or details, only the numbers."
        )
    except Exception as e:
        logger.error(f"Error during GPT API call: {e}")
        return {}
    
    try:
        gpt_response_list = [int(num) for num in gpt_response.split(", ")]
    except ValueError as e:
        logger.error(f"Error processing GPT response: {e}")
        return {}

    response = {}
    for key, value in news.items():
        if key in gpt_response_list:
            response[key] = value
    
    for key, value in response.items():
        try:
            value['content'] = mainGptAPI(
                text=value['content'],
                prompt="Make it a 3-4 word headline. Return only the reformatted text."
            )
        except Exception as e:
            logger.error(f"Error processing content for article {key}: {e}")
            value['content'] = "Error occurred while processing content."

    for key, value in response.items():
        try:
            value['description'] = mainGptAPI(
                text=f"{value['description']}, {value['content']}",
                prompt="Create a 30-40 simple word news-style text based on the provided information. Keep it concise, engaging, and clear for a general audience. Focus on the key details and make it easy to read. Return only the result."
            )
        except Exception as e:
            logger.error(f"Error processing content for description {key}: {e}")
            value['description'] = "Error occurred while processing content."

    for key, value in response.items():
        try:
            value['tags'] = mainGptAPI(
                text = f"{value['description']}, {value['content']}",
                prompt="Generate 2-4 popular and relevant hashtags based on the provided text. Focus on the main topics and trends related to the content. Return only the result."
            )
        except Exception as e:
            logger.error(f"Error processing content for description {key}: {e}")
            value['description'] = "Error occurred while processing content."    
    return response

def mainproc():
    try:
        news = mainNewsapi()
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        return {}

    return requestprocessing(news=news)
