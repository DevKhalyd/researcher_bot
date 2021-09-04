"""Handle the common utils for the bot functionality"""

import json
import os

KEY_TOKEN = 'TOKEN'
KEY_PORT = 'PORT'


def getBotToken() -> str:
    """Get the bot token according to the environment"""
    token = os.environ.get(KEY_TOKEN)
    if type(token) == str:
        return token

    token = getValueFromJsonFile(KEY_TOKEN)
    if type(token) == str:
        return token


def getPort():
    """Get the port to start to listen. If this one returns None means that the environment is local"""
    port = os.environ.get('PORT')
    return port


def getValueFromJsonFile(key, file='keys.json'):
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
