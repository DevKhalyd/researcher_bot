"""
A Reddit Scrapping Bot
"""
import logging

from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
from telegram import Update, ParseMode, MessageEntity

from utils import getBotToken, getPort
from values import REPLY_START, REPLY_HELP, REPLY_VERSION

# Enable logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def start(update: Update, _) -> None:
    """An introduction to the bot"""
    update.message.reply_text(REPLY_START, parse_mode=ParseMode.MARKDOWN_V2)


def help(update: Update, _) -> None:
    """Show all the avaible commands"""
    update.message.reply_text(REPLY_HELP, parse_mode=ParseMode.MARKDOWN_V2)


def version(update: Update, _) -> None:
    """Show all the avaible commands"""
    update.message.reply_text(REPLY_VERSION, parse_mode=ParseMode.MARKDOWN_V2)

def code(update: Update, _) -> None:
    """Shows where the code stored is"""
    msg = "Code store  at: https://github.com/DevKhalyd/researcher_bot/"
    update.message.reply_text(msg)


def echo(update: Update, context: CallbackContext) -> None:
    """Print a message sent by the user and delete the message who sent this one"""
    message = update.message
    update.message.delete()
    useMessage = message.text
    entities = message.parse_entities([MessageEntity.BOT_COMMAND])
    commandToDelete = None
    for _, v in entities.items():
        commandToDelete = v

    # NOTE: Migth be that here we need other statement to handle if this one is None
    if commandToDelete is not None:
        useMessage = useMessage.replace(commandToDelete, '')
    useMessage = f"*{useMessage}*"
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=useMessage,
                             parse_mode=ParseMode.MARKDOWN_V2)


def unknown(update, _) -> None:
    msg = "Sorry, I didn't understand that command. Run the command /help to see all commands"
    """When a command is sent and is not recognize"""
    update.message.reply_text(msg)


# TODO: FIX THIS MEHTOD
def file(update: Update, context: CallbackContext) -> None:
    """Depending of the type of file the bot send a response"""
    message = update.message
    isPhoto = len(message.photo or []) > 0
    isVideo = message.video is not None
    media_group_id = update.message.media_group_id

    shouldNotContinue = True

    if media_group_id is not None:
        chat_id = update._effective_chat.id
        chat_data = context.chat_data
        # Keys
        key_media = f'media_group_id_{chat_id}'
        key_was_sent_msg = 'msg_was_sent'
        # Logic to save and get the data
        media_group_id_last_saved = chat_data.get(key_media)
        # Retrieve the data or update depending of the case
        if media_group_id_last_saved is None:
            chat_data[key_media] = media_group_id
        else:
            # New set of files
            if media_group_id_last_saved != media_group_id:
                chat_data.update({
                    key_media: media_group_id,
                    key_was_sent_msg: False
                })

        was_sent_msg = chat_data.get(key_was_sent_msg, False)

        if not was_sent_msg:
            shouldNotContinue = False
            # The messaage was sent in this media group
    else:
        shouldNotContinue = False

    if shouldNotContinue:
        return

    # IMPROVE: Take a list of emojis and generate randomly
    if isPhoto:
        msg = '*Nice pic\(s\)\, dude\. 🥵*'
        update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN_V2)

    if isVideo:
        update.message.reply_text(
            "*Nice video\(s\)\, dude\.* 🥴 ", parse_mode=ParseMode.MARKDOWN_V2)

    if not isVideo and not isPhoto:
        update.message.reply_text(
            "*It's a virus?* 🐉 ", parse_mode=ParseMode.MARKDOWN_V2)

    if media_group_id is not None:
        chat_data.update({
            key_media: media_group_id,
            key_was_sent_msg: True
        })


def main() -> None:
    """Run the main process
    idle:
    Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    SIGABRT. This should be used most of the time, since start_polling() is
    non-blocking and will stop the bot gracefully.
    """
    TOKEN = getBotToken()
    PORT = getPort()
    NAME = 'researcher-bot'

    """Run Bot"""
    updater = Updater(token=TOKEN)

    # Init the dispatcher
    dispatcher = updater.dispatcher

    # Init the handlers
    start_handler = CommandHandler('start', start)
    echo_handler = CommandHandler('echo', echo)
    code_handler = CommandHandler('code', code)
    help_handler = CommandHandler('help', help)
    version_handler = CommandHandler('version', version)

    # Filter Handler
    file_handler = MessageHandler(Filters.video | Filters.photo | Filters.document,
                                  file)

    # This handler always should be the last to avoid bugs
    unknown_handler = MessageHandler(Filters.command, unknown)

    # Add the handlers to the dispatchers
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(code_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(file_handler)
    dispatcher.add_handler(version_handler)
    # This dispatcher always should be the last to avoid bugs
    dispatcher.add_handler(unknown_handler)

    # Start the webhook
    if PORT is not None:
        updater.start_webhook(listen="0.0.0.0",
                              port=int(PORT),
                              url_path=TOKEN,
                              webhook_url=f"https://{NAME}.herokuapp.com/{TOKEN}")
        updater.idle()
        return
    # Start the Bot usint the `getUpdates` API method
    updater.bot.delete_webhook()
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
