"""
A Reddit Scrapping Bot
"""
import logging
from datetime import datetime

from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
from telegram import Update, ParseMode, MessageEntity

from values import REPLY_START, REPLY_HELP, REPLY_VERSION
from utils import get_bot_token, get_port, allow_send_message, send_message_type

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


def file(update: Update, context: CallbackContext) -> None:
    """Listen when a video, image or file is send to the server then send a message to the user(s)"""
    key = f'date_{update.message.media_group_id}'
    chat_data = context.chat_data
    # Get the last date saved
    last_date = chat_data.get(key)
    currentDate = datetime.today().strftime('%X')

    # Send message according to the sort of message and assing the last_date
    if last_date is None:
        # Assign by first time
        chat_data[key] = currentDate
        send_message_type(update)
        return

    isAllowed = allow_send_message(last_date, currentDate)

    if not isAllowed:
        print('Not allowed')
        return
    # Send message according to the sort of message and update the last_message
    chat_data.update({
        key: currentDate
    })
    send_message_type(update)


def main() -> None:
    """Run the main process
    idle:
    Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    SIGABRT. This should be used most of the time, since start_polling() is
    non-blocking and will stop the bot gracefully.
    """
    TOKEN = get_bot_token()
    PORT = get_port()
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
