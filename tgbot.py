from environs import Env
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from google.cloud import dialogflow

env = Env()
env.read_env()


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Help!')


def detect_intent_texts(update: Update, context: CallbackContext):
    project_id = env('PROJECT_ID')
    language = env('BOT_LANGUAGE')
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, update.effective_user.id)
    text_input = dialogflow.TextInput(text=update.message.text, language_code=language)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    update.message.reply_text(response.query_result.fulfillment_text)


def main():
    updater = Updater(env('TELEGRAM_BOT_TOKEN'))
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, detect_intent_texts))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
