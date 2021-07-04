# Introducing

Hi guys. This is my first blog post, not only on this platform, but in general (And I write it using google.translate, sorry for mistakes). 
I really liked the idea of this platform, so I decided to give it a try.
I really love programming in python, although this is not my main area of work. Today I want to share with you one library for logging.

How do you prefer to write debug messages in your scripts? I usually use plain print, and that's usually enough.

But when the project gets more complex, all these prints posted all over the project can be terribly annoying, and they mess up the code.
In such cases, I prefer to include the loguru library in my project. It's a third party library, but I think it's worth adding to your project.

# Install

it is installed very simple 


```
pip install loguru
``` 

What I like the most about it is the color output in the console. I really like this feature.
But it also has a default log format set up, quite detailed, and in common you don't need to configure anything else.

Logs are of several levels
- trace
- debug
- info
- warning
- error
- critical

To write a message to the log, just call the function of the same name. 

# Simple example

Let's take a look at an example

```
from loguru import logger

bottles_count = 99
logger.debug(f"{bottles_count} bottles of beer on the wall, {bottles_count} bottles of beer. Take one down pass it around.")
bottles_count -= 1
logger.info(f"{bottles_count} bottles of beer on the wall, {bottles_count} bottles of beer. Take one down pass it around.")
bottles_count -= 1
logger.success(f"{bottles_count} bottles of beer on the wall, {bottles_count} bottles of beer. Take one down pass it around.")
bottles_count -= 1
logger.warning(f"{bottles_count} bottles of beer on the wall, {bottles_count} bottles of beer. Take one down pass it around.")
bottles_count -= 1
logger.error(f"{bottles_count} bottles of beer on the wall, {bottles_count} bottles of beer. Take one down pass it around.")
bottles_count -= 1
logger.critical(f"{bottles_count} bottles of beer on the wall, {bottles_count} bottles of beer. Take one down pass it around.")
```

The output is...
![image.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1625027059063/BNQCCEFZU.png)

You can also add your own levels, or override the colors of the standard levels using environment variables.

# Write logs to file

Setting up logging to a file is also simple

```
logger.add("my_wonderful.log")
```

But this is a simple case, but what if you want to separate the logs by time
```
logger.add("my_wonderful_{time}.log")
```
Not the best option. This will do one file for each milisecond, let's specify to do one file per day.
```
logger.add("my_wonderful_{time:YYYY_MM_DD}.log")
```

Excellent! 

And here are some more interesting options from the official documentation.
```
logger.add("file_1.log", rotation="500 MB") # Automatically rotate too big file
logger.add("file_2.log", rotation="12:00") # New file is created each day at noon
logger.add("file_3.log", rotation="1 week") # Once the file is too old, it's rotated
logger.add("file_X.log", retention="10 days") # Cleanup after some time
logger.add("file_Y.log", compression="zip") # Save some loved space
```

# Change format of logs

Unfortunately, there is no method in loguru that would allow you to simply change the format of the log messages, so to do this, you first need to delete the logger created by import,
and then add a new one indicating the format

```
import sys
from loguru import logger

logger.remove()
logger.add(sys.stderr, colorize=True, format=" <level>{level}</level>| <magenta>{time:YYYY-MM-DD}</magenta>| <level>{message}</level>)")

bottles_count = 99
logger.debug(f"{bottles_count} bottles of beer on the wall, {bottles_count} bottles of beer. Take one down pass it around.")
bottles_count -= 1
logger.info(f"{bottles_count} bottles of beer on the wall, {bottles_count} bottles of beer. Take one down pass it around.")
bottles_count -= 1
logger.success(f"{bottles_count} bottles of beer on the wall, {bottles_count} bottles of beer. Take one down pass it around.")
bottles_count -= 1
logger.warning(f"{bottles_count} bottles of beer on the wall, {bottles_count} bottles of beer. Take one down pass it around.")
bottles_count -= 1
logger.error(f"{bottles_count} bottles of beer on the wall, {bottles_count} bottles of beer. Take one down pass it around.")
bottles_count -= 1
logger.critical(f"{bottles_count} bottles of beer on the wall, {bottles_count} bottles of beer. Take one down pass it around.")
```

The output is ...
![image.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1625027406524/sLxGT-hxJ.png)

# Binding variables

We can even use variables in the logs. 
To do this, you need to set your own format with additional variables using dictionary **extra**.
For example..
```
logger.add(sys.stderr, colorize=True, 
format=" <level>{level}</level>| {extra[user_id]}| <magenta>{time:YYYY-MM-DD}</magenta>| <level>{message}</level>")
```
And now you need to use the logger like this
```
logger.debug("enter the system", user_id="007")
```
But in order not to enter the value of the variable every time, you can bind it to the logger, this is much cleaner
```
logger = logger.bind(user_id="007")
logger.debug("enter the system")
logger.warning("get access to secret information")
logger.critical("installing danger program")
```

![image.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1625126455155/L9Luf5r6S.png)

Or you can make several context loggers, with different variables
```
logger1 = logger.bind(user_id="007")
logger2 = logger.bind(user_id="001")
logger1.debug("enter the system")
logger2.debug("checking user documents")
```

![image.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1625126549106/V70KOjBOc.png)

# Custom log handler

And what if you want to do some special processing of the logs, you can split files depending on binded variables, send reports to the mail or write records to the database in some cases.
To do this, you can very simply write your own function, and connect it as a message handler (sink)

```
def send_mail_to_admin(s):
    print("mail to admin " + s, end='')

def urgent_call_to_admin(s):
    print("call to admin " + s, end='')

ADMIN_ID = [123]

def my_weird_logger(message):
    # message.record - dict with message data
    if message.record["extra"]["user_id"] in ADMIN_ID:
        return
    
    if message.record["level"].no >= 40:
        send_mail_to_admin(message)

    if "DB IS OFFLINE" in message:
        urgent_call_to_admin(message)

logger.add(my_weird_logger)
```

Let's try it
```
logger = logger.bind(user_id=222)
logger.debug("enter the system")
logger.error("can't find file .....")
logger.critical("DB IS OFFLINE")
```

![image.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1625127659474/A6ONHoEWW.png)

# Notifiers 

Well, in addition, you can use the wonderful  [notifiers](https://github.com/liiight/notifiers)  library (installed separately), in which many different notification options are already configured

```
import notifiers

params = {
    "username": "you@gmail.com",
    "password": "abc123",
    "to": "dest@gmail.com"}

# Send a single notification
notifier = notifiers.get_notifier("gmail")
notifier.notify(message="The application is running!", **params)

# Be alerted on each error message
from notifiers.logging import NotificationHandler
handler = NotificationHandler("gmail", defaults=params)
logger.add(handler, level="ERROR")
```

# Loguru official documentation

-  [Overview](https://loguru.readthedocs.io/en/stable/overview.html) 
-  [Help & Guides ](https://loguru.readthedocs.io/en/stable/resources.html) 

# Conclussion

I really hope that the information was interesting and useful for you.
Use loguru in your projects. It's very cool.

See you.