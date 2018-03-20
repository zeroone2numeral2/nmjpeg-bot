import logging
from telegram.ext import CommandHandler
from telegram.ext import BaseFilter
from telegram.ext.dispatcher import run_async
from telegram import ParseMode

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

@run_async
def send_help(bot, update):
	logger.info("start or help command")
	bot.send_message(update.message.chat_id, help_message,
		parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

class module:
	name = "help"
	handlers = (
		CommandHandler(["start", "help"], send_help),
	)