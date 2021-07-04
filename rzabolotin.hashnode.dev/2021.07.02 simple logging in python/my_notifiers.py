# 9.
from loguru import logger
import notifiers
from notifiers.logging import NotificationHandler

params = {
    "username": "you@gmail.com",
    "password": "abc123",
    "to": "dest@gmail.com"}

# Send a single notification
notifier = notifiers.get_notifier("gmail")
notifier.notify(message="The application is running!", **params)

# Be alerted on each error message

handler = NotificationHandler("gmail", defaults=params)
logger.add(handler, level="ERROR")