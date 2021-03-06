import random
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from environs import Env
from google.cloud import dialogflow
import telegram
import logging
from tg_log_handler import TelegramLogsHandler

env = Env()
env.read_env()


def detect_intent_texts(event, vk_api):
    project_id = env('PROJECT_ID')
    language = env('BOT_LANGUAGE')
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, event.user_id)
    text_input = dialogflow.TextInput(text=event.text, language_code=language)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    if response.query_result.intent.is_fallback:
        return None
    vk_api.messages.send(
        user_id=event.user_id,
        message=response.query_result.fulfillment_text,
        random_id=random.randint(1, 1000)
    )


if __name__ == "__main__":
    logger = logging.getLogger('vk_bot')
    logger.setLevel(logging.INFO)
    logger_bot = telegram.Bot(token=env('LOGGER_TELEGRAM_TOKEN'))
    logger.addHandler(TelegramLogsHandler(logger_bot, chat_id=env('TG_CHAT_ID')))
    logger.info('VK бот запущен')
    try:
        vk_session = vk.VkApi(token=env('VK_BOT_TOKEN'))
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                detect_intent_texts(event, vk_api)
    except Exception as error:
        logger.info('VK бот упал с ошибкой:')
        logger.exception(error)
