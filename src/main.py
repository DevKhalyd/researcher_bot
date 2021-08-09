"""
Simple Bot to reply to Telegram bots
"""

# Just print basic thing in the console
import logging

from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
from telegram import Update
from datetime import time
from pytz import timezone

bot_token = '1923146736:AAG9u9kHT-L7bYrcQaP-iRSm12f8fXfojwg'

# Enable logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def start(update: Update, _: CallbackContext) -> None:
    """Sends explanation on how to use the bot."""
    update.message.reply_text(
        "Hi! By now I don't have many features because I'm small. But check the command /todo to help to develop me")


def todo(update: Update, _) -> None:
    msg = """
        1. Make some web scrapping
        2. Get links to show in chat
        3. Rate the content
        4. Get the latest info about each topic
        5. Make some validations. For example, if the bot is not inside of my favorite group
        change some lines of the code
    """
    update.message.reply_text(msg)


def code(update: Update, _) -> None:
    msg = "Code at: https://github.com/DevKhalyd/researcher_bot/"
    update.message.reply_text(msg)


def echo(update, context: CallbackContext) -> None:
    """Print a message sent by the user"""
    # Get the last message
    useMessage = update.message.text.replace('/echo@reply_msgs_bot', '')

    if not useMessage:
        useMessage = "Missing word to echo"

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=useMessage)


def cris(update: Update, _) -> None:
    """A friendly message"""
    update.message.reply_text('@EKO0032 CTM we')


def unknown(update, context) -> None:
    """When a command is sent and is not recognize"""
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Sorry, I didn't understand that command. Run the command /help to see all commands")


def daily_job(context: CallbackContext) -> None:
    context.bot.send_message(chat_id='288386043',
                             text='One message every day')


def main() -> None:
    """Run Bot"""
    updater = Updater(token=bot_token)
    # Init the JobQueue
    jobQueue = updater.job_queue

    # Init the dispatcher
    dispatcher = updater.dispatcher
    # NOTE: Example of the job queue
    # jobQueue.run_repeating(daily_job, interval=10, first=10)

    mexico = timezone('America/Mexico_City')

    timeToExecute = time(hour=23, minute=30, tzinfo=mexico)
    # NOTE: Validation if the chat corresponds to the group id send it.
    jobQueue.run_daily(daily_job, time=timeToExecute)

    # Init the handlers
    start_handler = CommandHandler('start', start)
    echo_handler = CommandHandler('echo', echo)
    info_handler = CommandHandler('code', code)
    todo_handler = CommandHandler('todo', todo)
    cris_handler = CommandHandler('cris', cris)
    unknown_handler = MessageHandler(Filters.command, unknown)

    # Add the handlers to the dispatchers
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(info_handler)
    dispatcher.add_handler(todo_handler)
    dispatcher.add_handler(cris_handler)
    # This handler always should be the last to avoid bugs
    dispatcher.add_handler(unknown_handler)

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
