import os
import logging
import importlib

from telegram.ext import Updater

updater = Updater(token=os.environ.get('TG_TOKEN') or "")
dispatcher = updater.dispatcher

logging.basicConfig(format='[%(asctime)s][%(name)s][%(levelname)s] %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def main():
    for modname in ["compressor", "help"]:
        module = getattr(importlib.import_module('modules.{}'.format(modname)), "module")  # from modules.modname import module
        logger.info("importing module: %s (handlers: %d)", module.name, len(module.handlers))
        for handler in module.handlers:
            dispatcher.add_handler(handler)

    updater.start_polling(clean=True)
    updater.idle()


if __name__ == '__main__':
    main()
