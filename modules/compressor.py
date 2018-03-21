import os
import sys
import logging
from telegram.ext import MessageHandler
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import BaseFilter
from telegram.ext.dispatcher import run_async
from picture import Picture

logger = logging.getLogger(__name__)

BASE_FILE_PATH = os.path.abspath(os.path.dirname(sys.argv[0])) + '/tmp/{}_{}.jpg'

class FilterReplyToPhoto(BaseFilter):
	def filter(self, message):
		if message.reply_to_message and message.reply_to_message.photo:
			return True

class FilterPrivateChat(BaseFilter):
	def filter(self, message):
		return message.chat_id > 0

private_chat = FilterPrivateChat()
photo_reply = FilterReplyToPhoto()

class PictureExtended(Picture):
	def __init__(self, message, quality=20):
		if message.reply_to_message:
			self.PhotoSize_object = message.reply_to_message.photo[-1]
			self.reply_to_message_id = message.reply_to_message.message_id
		else:
			self.PhotoSize_object = message.photo[-1]
			self.reply_to_message_id = None

		self.chat_id = message.chat_id
		self.message_id = message.message_id
		self.file_path = BASE_FILE_PATH.format(self.chat_id, self.message_id)
		self.message = message
		Picture.__init__(self, self.file_path, quality=quality)

	def download(self):
		new_file = self.PhotoSize_object.bot.get_file(self.PhotoSize_object.file_id)
		new_file.download(self.file_path)

	def send(self):
		with open(self.compressed_file_path, 'rb') as file:
			self.message.reply_photo(file, reply_to_message_id=self.reply_to_message_id)

	def one_shot(self):
		self.download()
		self.load()
		self.compress()
		self.send()
		self.remove()

@run_async
def on_photo_private(bot, update):
	logger.info("private chat photo")

	PictureExtended(update.message).one_shot()

def get_quality_level(args):
	if len(args) > 0:
		try:
			quality_level = int(args[0])
			if quality_level > 99:
				quality_level = 99
			elif quality_level < 1:
				quality_level = 1
		except ValueError:
			quality_level = 20
	else:
		quality_level = 20

	return quality_level

@run_async
def on_command(bot, update, args):
	logger.info("jpeg command")

	quality_level = get_quality_level(args)
	logger.info("quality level: %d", quality_level)

	PictureExtended(update.message, quality=quality_level).one_shot()

class module:
	name = "compressor"
	handlers = (
		MessageHandler(Filters.photo & private_chat, on_photo_private),
		CommandHandler(["morejpg", "morejpg", "nmjpg", "nmjpeg", "jpg", "jpeg"],
			on_command, filters=photo_reply, pass_args=True)
	)