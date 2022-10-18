from aiogram import types

import config
from dispatcher import dp, bot


@dp.message_handler(content_types=['new_chat_members'])
async def send_welcome(message: types.Message):
    me = await bot.get_me()
    # if message.new_chat_participant.id == me.id:
    for chat_member in message.new_chat_members:
        if chat_member.id == me.id and message.chat.id not in config.chat_id:
            await message.answer("Привет!\nЭто группа не находится в списке разрешенных!\nБот будет удален!")
            await bot.leave_chat(chat_id=message.chat.id)
        else:
            await message.delete()


@dp.message_handler(content_types=["voice"])
async def voice_message(message: types.Message):
    await message.delete()


@dp.message_handler(content_types=["voice"])
async def voice_message(message: types.Message):
    await message.delete()


@dp.message_handler(content_types=["left_chat_member"])
async def user_left_chat(message: types.Message):
    await message.delete()


@dp.message_handler(content_types=["any"])
async def delete_anon_channel(message: types.Message):
    if message.from_user.first_name == "Channel" and message.sender_chat.id not in config.channel_whitelist:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
