# TODO

1. Update the telegram commnands with BotFather...
2. Update the version each time the bot is updated

# Telegram Basic Bot

Use an environment to avoid crash between libraries

Docs:

https://python-telegram-bot.readthedocs.io/en/stable/

## What to do when updates the code?

1. Update the commands in Telegram Father

2. Update in Heroku

## Documentation

**Wiki**
https://github.com/python-telegram-bot/python-telegram-bot/wiki

**Code-snipperts**
https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets

## Consider:

`pip install python-telegram-bot[passport]` installs the cryptography library. Use this, if you want to use Telegram Passport related functionality.

`pip install python-telegram-bot[ujson]` installs the ujson library. It will then be used for JSON de- & encoding, which can bring speed up compared to the standard json library.

`pip install python-telegram-bot[socks]` installs the PySocks library. Use this, if you want to work behind a Socks5 server.

## Resources

**MAKRDOWN V2**

Correct use:

https://stackoverflow.com/questions/62230148/python-telegram-bot-markdown

Oficial Docs:

https://core.telegram.org/bots/api#markdownv2-style

**Emojis Supported by GitHub**

https://gist.github.com/rxaviers/7360908

or If you are on Windows use:

`Windows` + `.` 👌

**The time zones in the world**
https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

**Test the bot in a local environment**
https://devcenter.heroku.com/articles/heroku-local

```python
    mexico = timezone('America/Mexico_City')
    timeToExecute = time(hour=23, minute=30, tzinfo=mexico)
    # NOTE: Validation if the chat corresponds to the group id send it.
    # Import those libraries and check the repository...
    from datetime import time
    from pytz import timezone
    #Handle the time in Mexico City
    jobQueue.run_daily(daily_job, time=timeToExecute)
```

# Deploy

git push heroku main