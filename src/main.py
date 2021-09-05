"""
By the moment  a little bot  I hope I an few months will be a big bot
"""

# Just print basic thing in the console
import logging

from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
from telegram import Update, ParseMode, MessageEntity
from datetime import time
from pytz import timezone

from utils import getBotToken, getPort
from values import REPLY_TODO, REPLY_WAKE_UP, REPLY_START

# Enable logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def wake_up(update: Update, _):
    """Basically this method prepares the bot to start to fetch commands"""
    update.message.reply_text(REPLY_WAKE_UP, parse_mode=ParseMode.MARKDOWN_V2)


def start(update: Update, _) -> None:
    """Sends explanation on how to use the bot."""
    update.message.reply_text(REPLY_START, parse_mode=ParseMode.MARKDOWN_V2)


def todo(update: Update, _) -> None:
    """What to do to help to develop this bot"""
    update.message.reply_text(REPLY_TODO, parse_mode=ParseMode.MARKDOWN_V2)


def code(update: Update, _) -> None:
    msg = "Code store  at: https://github.com/DevKhalyd/researcher_bot/"
    update.message.reply_text(msg)


def echo(update: Update, context) -> None:
    """Print a message sent by the user"""
    message = update.message
    update.message.delete()
    useMessage = message.text
    entities = message.parse_entities([MessageEntity.BOT_COMMAND])
    commandToDelete = None
    for _, v in entities.items():
        commandToDelete = v

    if commandToDelete is not None:
        useMessage = useMessage.replace(commandToDelete, '')
    # NOTE: Migth be that here we need other statement to handle if this one is None
    useMessage = f"*{useMessage}*"
    #update.message.reply_text(useMessage, parse_mode=ParseMode.MARKDOWN_V2)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=useMessage,
                             parse_mode=ParseMode.MARKDOWN_V2)


def unknown(update, context) -> None:
    """When a command is sent and is not recognize"""
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Sorry, I didn't understand that command. Run the command /help to see all commands")


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
    todo_handler = CommandHandler('todo', todo)
    wake_up_handler = CommandHandler('wakeup', wake_up)

    # This handler always should be the last to avoid bugs
    unknown_handler = MessageHandler(Filters.command, unknown)

    # Add the handlers to the dispatchers
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(code_handler)
    dispatcher.add_handler(todo_handler)
    dispatcher.add_handler(wake_up_handler)

    # This handler always should be the last to avoid bugs
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
