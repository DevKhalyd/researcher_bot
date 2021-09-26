"""Handle the common utils for the bot functionality"""
from typing import Union, List
import random
import json
import os

from functools import wraps
from telegram import Update, ParseMode, ChatAction, InlineKeyboardButton

KEY_TOKEN = 'TOKEN'
KEY_PORT = 'PORT'


def get_bot_token() -> str:
    """Get the bot token according to the environment"""
    token = os.environ.get(KEY_TOKEN)
    if type(token) == str:
        return token

    token = get_value_from_json(KEY_TOKEN)
    if type(token) == str:
        return token


def get_port():
    """Get the port to start to listen. If this one returns None means that the environment is local"""
    port = os.environ.get('PORT')
    return port


def allow_send_message(d1: str, d2: str) -> bool:
    """
    Get the difference between two hours given and return True if allow to send a message
    :param str d1: The initial date
    :param str d2: The final date
    return: If is allowed to send a message
    rtype: True
    """
    itemsD1 = d1.split(':')
    itemsD2 = d2.split(':')

    if len(itemsD1) != len(itemsD2):
        return True

    hourD1 = int(itemsD1[0])
    hourD2 = int(itemsD2[0])

    # Not the same hour
    if hourD1 != hourD2:
        return True

    minuteD1 = int(itemsD1[1])
    minuteD2 = int(itemsD2[1])

    difference = minuteD2 - minuteD1

    if difference < 0:
        return True
    # Minutes to send another message
    return difference > 0


def get_value_from_json(key, file='keys.json'):
    """Get a value from a json file a handle the errors. Could return None"""
    try:
        f = open(file)
        data = json.load(f)
        value = data[key]
        f.close()
        return value
    except:
        raise ValueError(
            f'${key} is not defined. Please verify the environment')


def send_message_type(update: Update):
    """Send message according to the type of message (Image,Video,File)"""
    # NOTE: Also a job can help to send this message
    message = update.message
    isPhoto = len(message.photo or []) > 0
    isVideo = message.video is not None
    isFile = not isVideo and not isPhoto

    # IMPROVE: Take a list of emojis and generate randomly
    if isPhoto:
        msg = f'*Nice {definition_image()}, dude\.* {generate_emoji()}'
        update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN_V2)

    if isVideo:
        update.message.reply_text(
            f"*Nice {definition_video()}, dude\.* {generate_emoji()} ", parse_mode=ParseMode.MARKDOWN_V2)

    if isFile:
        update.message.reply_text(
            f"*It's a virus?* {generate_emoji()}", parse_mode=ParseMode.MARKDOWN_V2)


def generate_emoji():
    """Generates a emoji randomly"""
    emojis = ['🥴', '🤔', '👿', '🥳', '🥵', '😎', '👾', '🥶', '🤩']
    n = random.randint(0, len(emojis) - 1)
    return emojis[n]


def definition_image():
    """Get a image definition"""
    imgs = ['img', 'pic', '\.jpg', '\.png']
    n = random.randint(0, len(imgs) - 1)
    return imgs[n]


def definition_video():
    """Get a video  definition"""
    videos = ['video', '\.mp4', 'videou']
    n = random.randint(0, len(videos) - 1)
    return videos[n]

# Ref: https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#send-a-chat-action
#  context.bot.send_chat_action(chat_id=update.effective_chat.id,
#                                  action=ChatAction.TYPING
#                                  )

def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(
            chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(update, context,  *args, **kwargs)

    return command_func

def build_menu(
    buttons: List[InlineKeyboardButton],
    n_cols: int,
    header_buttons: Union[InlineKeyboardButton, List[InlineKeyboardButton]]=None,
    footer_buttons: Union[InlineKeyboardButton, List[InlineKeyboardButton]]=None
) -> List[List[InlineKeyboardButton]]:
    """
    Build a menu with Buttons
    Ref: https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#build-a-menu-with-buttons
    """
    # Behavior of [i:i]
    # https://stackoverflow.com/questions/59060606/in-python-why-is-listii-n-insert-an-element-in-listii
    # https://docs.python.org/3/library/stdtypes.html?highlight=list#mutable-sequence-types
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons if isinstance(header_buttons, list) else [header_buttons])
    if footer_buttons:
        menu.append(footer_buttons if isinstance(footer_buttons, list) else [footer_buttons])
    return menu

