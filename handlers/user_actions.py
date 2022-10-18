from aiogram import types

import config
from dispatcher import dp


@dp.message_handler(commands=[config.custom_message_command[1:]], commands_prefix=config.custom_message_command[0])
async def custom_message(message: types.Message):
    await message.answer(config.custom_message)
