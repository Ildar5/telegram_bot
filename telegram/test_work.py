from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler, MessageHandler, Filters
from env import environment
from telegram import audio_message as aum
from telegram import photo_message as pm


env = environment.Environment().get_env()
TELEGRAM_API_TOKEN = env['TELEGRAM_API_TOKEN']
updater = Updater(token=env['TELEGRAM_API_TOKEN'], use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=env['START_MESSAGE'])


def echo(update, context):
    print(update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def audio(update, context):
    print('Voice Message:')
    aum.AudioMessage().audio(update, 'voice_message')


def photo(update, context):
    print('Photo:')
    pm.PhotoMessage().photo(update, 'photo')


def document(update, context):
    print('Document:')
    document = update.message.document
    mime_type = document.mime_type.split('/')[0]
    if mime_type == 'image':
        pm.PhotoMessage().photo(update, 'photo_file')


def audio_file_format(update, context):
    print('Audio Message:')
    aum.AudioMessage().audio(update, 'audio_file')


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

audio_handler = MessageHandler(Filters.voice, audio)
dispatcher.add_handler(audio_handler)

photo_handler = MessageHandler(Filters.photo, photo)
dispatcher.add_handler(photo_handler)

document_handler = MessageHandler(Filters.document, document)
dispatcher.add_handler(document_handler)

audio_handler = MessageHandler(Filters.audio, audio_file_format)
dispatcher.add_handler(audio_handler)

updater.start_polling()
