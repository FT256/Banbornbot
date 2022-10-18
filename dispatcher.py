import logging
from aiogram import Bot, Dispatcher

import config
from filters import IsAdminFilter

# Configure logging
logging.basicConfig(level=logging.INFO)

if not config.token:
    logging.error("No token provided")
    exit(1)

# Initialize bot and dispatcher
bot = Bot(token=config.token, parse_mode="HTML")
dp = Dispatcher(bot)

# Activate filters
dp.filters_factory.bind(IsAdminFilter)