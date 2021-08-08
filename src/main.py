"""
Simple Bot to reply to Telegram bots
"""

# Just print basic thing in the console

import logging

from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
from telegram import Update

bot_token = '1923146736:AAG9u9kHT-L7bYrcQaP-iRSm12f8fXfojwg'

# Enable logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def start(update: Update, context: CallbackContext) -> None:
    """Sends explanation on how to use the bot."""
    update.message.reply_text(
        "Hi! By now I don't have features because I'm small. But check the command /todo to help to develop me")


def todo(update, _: CallbackContext) -> None:
    msg = """
        1. Make some web scrapping
        2. Get links to show in chat
        3. Rate the content
        4. Get the latest info about each topic
    """
    update.message.reply_text(msg)


def info(update, context: CallbackContext) -> None:
    msg = "Code is stored at GitHub.com. Check: Missing Url"
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=msg
    )


def echo(update, context: CallbackContext) -> None:
    # Get the last message
    useMessage = update.message.text.replace('/echo@reply_msgs_bot', '')
    

    if not useMessage:
        useMessage = "Your missing a word to print"

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=useMessage)

def unknown(update, context) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Sorry, I didn't understand that command.")
                   
def main() -> None:
    """Run Bot"""
    updater = Updater(token=bot_token)

    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    echo_handler = CommandHandler('echo', echo)
    info_handler = CommandHandler('info', info)
    todo_handler = CommandHandler('todo', todo)
    unknown_handler = MessageHandler(Filters.command, unknown)
    # Dispachers
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(info_handler)
    dispatcher.add_handler(todo_handler)
    dispatcher.add_handler(unknown_handler)

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
