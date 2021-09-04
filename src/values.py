

REPLY_START = '''
Type /todo to check what to do to help to develop the bot
Type /wakeup If the bot does not reply to your questions
'''

# Prepare the bot
REPLY_WAKE_UP = """
*Hits his ciber\-face*
Sir I'm ready 🏃‍♂️\!\!\!
"""

# Task to do in this bot
REPLY_TODO = '''
# TODO

## Web Scrapping (Handle by `smart` command)

   - Optional (**Paramerter** as `str`) : `website`. The website desired by the user to start the search.
   - Optional(**Parameter** as `int`): `limit`. The limit of search results. Default 3. Max: 10. This because telegram ask for quick results. Also could be the number of threads allowed by Python.
   - Required (**Parameter** as `str`): The input by the user. No more than 30 characters.

**Requirements:** Threads, Asynchronous methods, Data Structures, APIS and libraries. Check out the compatibility with the server. If some trouble is present use Docker instead of the default files.

**Goals:**

1. The user use the command defined then the bot return the `limit` of result.

2. The bot says: **Hey choose a result that you want to see between the 1 and the `limit`**. User picks one number.

3. Underground the bot go to search that result choosed by the user.

4. Depending on the page and the methods provided by the library return a bunch of result(s) to the user.


## JobQueue (Handle by `smart` command)

**Requirements:** Threads, Asynchronous methods, Data Structures, APIS and libraries.

**Goals:**

1. Basic implementation of a JobQueue. For example: A common message at the night

2. Implement a jobqueue for criptocurrency from this [API](https://www.coingecko.com/api/documentations/v3#/)

3. Implementation of another APIs that can be used with the JobQueue

# Where to start?

Check out the [docs](https://github.com/python-telegram-bot/python-telegram-bot/wiki)

Once time you can continue with the [Code Snippets](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets)

**NOTE**

Those tasks are just ideas that can be change with the time. Could be removed or added more depending on the case and support by the community.
'''
