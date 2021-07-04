import sys
from loguru import logger

# 1.
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


# 2.
logger.add("my_wonderful_{time:YYYY_MM_DD}.log")

# 3.
logger.add("file_1.log", rotation="500 MB") # Automatically rotate too big file
logger.add("file_2.log", rotation="12:00") # New file is created each day at noon
logger.add("file_3.log", rotation="1 week") # Once the file is too old, it's rotated
logger.add("file_X.log", retention="10 days") # Cleanup after some time
logger.add("file_Y.log", compression="zip") # Save some loved space

# 4.


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

# 5.
logger.add(sys.stderr, colorize=True,
           format=" <level>{level}</level>| {extra[user_id]}| <magenta>{time:YYYY-MM-DD}</magenta>| <level>{message}</level>"
           )

logger.debug("enter the system", user_id="007")

logger = logger.bind(user_id="007")
logger.debug("enter the system")
logger.warning("get access to secret information")
logger.critical("installing danger program")

# 6.
logger1 = logger.bind(user_id="007")
logger2 = logger.bind(user_id="001")
logger1.debug("enter the system")
logger2.debug("checking user documents")


# 7.
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

# 8.
logger = logger.bind(user_id=222)
logger.debug("enter the system")
logger.error("can't find file .....")
logger.critical("DB IS OFFLINE")




