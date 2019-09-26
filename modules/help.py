import logging

from telegram.ext import CommandHandler
from telegram.ext import BaseFilter

logger = logging.getLogger(__name__)


class FilterPrivateChat(BaseFilter):
    def filter(self, message):
        return message.chat_id > 0


private_chat = FilterPrivateChat()

help_message = """\
[Needs more JPEG](http://knowyourmeme.com/memes/needs-more-jpeg) bot

*Private chat*: send a photo
*Group chat*: reply to a photo with `/morejpeg`
Pass a value from 1 to 99 to define the quality level, eg. "`/nmjpg 20`" (works in private too)
Command shortcuts: `/nmjpeg, /morejpeg, /jpeg` (the "e" in "jpeg" is optional)

[source code](https://github.com/zeroone2numeral2/nmjpeg-bot)\
"""


def send_help(_, update):
    logger.info("start or help command")
    update.message.reply_markdown(help_message, disable_web_page_preview=True)


class module:
    name = "help"
    handlers = (
        CommandHandler(["start", "help"], send_help),
    )
