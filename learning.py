from google.cloud import dialogflow
from google.api_core.exceptions import InvalidArgument
from environs import Env
import argparse
import json
import logging


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)

    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    answer_phrases = [message_texts]
    text = dialogflow.Intent.Message.Text(text=answer_phrases)
    message = dialogflow.Intent.Message(text=text)
    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )
    intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )


if __name__ == '__main__':
    env = Env()
    env.read_env()
    project_id = env('PROJECT_ID')
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', default='questions.json')
    args = parser.parse_args()
    logger = logging.getLogger('learning')
    try:
        with open(args.filename, 'r', encoding='utf-8') as file:
            file_contents = json.load(file)
        for intent_name, training_data in file_contents.items():
            create_intent(project_id, intent_name, training_data['questions'], training_data['answer'])
    except Exception as error:
        logger.exception(error)
