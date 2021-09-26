"""
A Reddit Scrapping Bot
"""
import logging
from datetime import datetime
from typing import List

from telegram.ext import (
    Updater,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    Filters,
)
from telegram import (
    Update, ParseMode,
    MessageEntity,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from utils import (
    get_bot_token,
    get_port,
    allow_send_message,
    send_message_type,
    send_typing_action,
    build_menu,
)

from values import LIST, REPLY_START, REPLY_HELP, REPLY_VERSION

from reddit_item import RedditItem

from scrapping import get_reddit_search_url, get_results_from_reddit

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


def unknown(update: Update, _) -> None:
    msg = "Sorry, I didn't understand that command. Run the command /help to see all commands"
    """When a command is sent and is not recognized"""
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


def file(update: Update, context: CallbackContext) -> None:
    """Listen when a video, image or file is send to the server then send a message to the user(s)"""
    key = f'date_{update.message.media_group_id}'
    chat_data = context.chat_data
    # Get the last date saved
    last_date = chat_data.get(key)
    currentDate = datetime.today().strftime('%X')

    # Send message according to the sort of message and assign the last_date
    if last_date is None:
        # Assign by first time
        chat_data[key] = currentDate
        send_message_type(update)
        return

    isAllowed = allow_send_message(last_date, currentDate)

    if not isAllowed:
        return
    # Send message according to the sort of message and update the last_message
    chat_data.update({key: currentDate})
    send_message_type(update)

# Use instead the manually method
# @send_typing_action

# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Storing-bot,-user-and-chat-related-data
@send_typing_action
def search(update: Update, context: CallbackContext) -> None:
    """Scrapping on Reddit and send the fetched results"""

    args = context.args

    if not args:
        msg = "The search param can't be empty"
        update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN_V2)
        return

    # Contains the data to search
    lookup = ""

    for i, arg in enumerate(args):
        lookup += arg
        lookup += "" if i == (len(args) - 1) else "%20"

    results = get_results_from_reddit(lookup)

    if not results:
        update.message.reply_text('Try with another phrase. Results not found')
        return

    button_list = [
        InlineKeyboardButton("See more", callback_data=lookup),
    ]

    total_to_send = len(results) // 2
    items_remaining : List[RedditItem] = []
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))

    for i,item in enumerate(results):
        if i < total_to_send:
            # Send messages
            update.message.reply_text(item.convert_to_telegram_msg())
        elif i == total_to_send:
            # Message with action
            update.message.reply_text(item.convert_to_telegram_msg(),reply_markup=reply_markup)
        else:
            # Save items for later
            items_remaining.append(item)
    
    items_string = RedditItem.convert_list_to_string(items_remaining)
    chat_data = context.chat_data
    chat_data.update({f'{LIST}{lookup}':items_string})


def search_query_handler_callback(update: Update, context: CallbackContext) -> None:
    """Handle the search command responses"""

    def final_response(lookup : str)->None:
        # CallbackQueries need to be answered, even if no notification to the user is needed
        # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
        query.answer()
        query.edit_message_text(text=f"If you wanna see more: {get_reddit_search_url(lookup)}")

    query = update.callback_query
    lookup = query.data
    
    chat_data = context.chat_data

    items_string = chat_data.get(f'{LIST}{lookup}')

    print(items_string)

    if not items_string:
        final_response(lookup)
        return
    
    items = RedditItem.convert_string_to_list(items_string)

    if not items:
        final_response(lookup)
        return
    
    for item in items:
        msg = item.convert_to_telegram_msg()
        if msg is not None:
            context.bot.send_message(chat_id=update.effective_chat.id,
                             text=msg)
    
    final_response(lookup)
    chat_data.clear()

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
    search_handler = CommandHandler('search', search)
    search_query_handler = CallbackQueryHandler(search_query_handler_callback)
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
    dispatcher.add_handler(search_handler)
    dispatcher.add_handler(search_query_handler)
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
