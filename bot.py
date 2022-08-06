import config
import filters
import logging
import utils

from time import time
import aiogram
from aiogram import Bot, Dispatcher, executor, types
from filters import IsAdminFilter

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=config.token)
dp = Dispatcher(bot)

# Activate custom filters
dp.filters_factory.bind(IsAdminFilter)

@dp.message_handler(content_types=['new_chat_members'])
async def send_welcome(message: types.Message):
    me = await bot.get_me()
    #if message.new_chat_participant.id == me.id:
    for chat_member in message.new_chat_members:
        if chat_member.id == me.id and message.chat.id not in config.chat_id:
            await message.answer("Привет!\nЭто группа не находится в списке разрешенных!\nБот будет удален!")
            await bot.leave_chat(chat_id=message.chat.id)
        else:
            await message.delete()

@dp.message_handler(content_types=["voice"])
async def voice_message(message: types.Message):
    await message.delete()

@dp.message_handler(content_types=["left_chat_member"])
async def user_left_chat(message: types.Message):
    await message.delete()
    
@dp.message_handler(commands=[config.call_admin_command[1:]], commands_prefix=config.call_admin_command[0])
async def call_admins(message: types.Message):
    await message.answer(config.call_admin_message)

@dp.message_handler(is_admin=True, commands=['ban'], commands_prefix="!")
async def cmd_ban(message: types.Message):
    if not message.reply_to_message:	
        await message.reply("Эта команда должна быть ответом на сообщение")
        return
    f_name = message.reply_to_message.from_user.first_name
    l_name = message.reply_to_message.from_user.last_name
    username = message.reply_to_message.from_user.username
    
    user = await message.bot.get_chat_member(message.chat.id, 
                                             message.reply_to_message.from_user.id
                                            )
    if user.is_chat_admin():
        await message.reply("Нельзя забанить администратора!")
        return

    if l_name == None:
        await message.answer(f"Пользователь {f_name} (@{username}) забанен навсегда!")
    else:
        await message.answer(f"Пользователь {f_name} {l_name} (@{username}) забанен навсегда!")
    await message.bot.delete_message(message.chat.id, message.message_id)# remove admin message
    await message.bot.kick_chat_member(chat_id=message.chat.id, 
                                       user_id=message.reply_to_message.from_user.id
                                      )

@dp.message_handler(is_admin=True, commands=["unban"], commands_prefix="!")
async def cmd_unban(message: types.Message):
    # Check if command is sent as reply to some message
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение")
        return

    user = await message.bot.get_chat_member(message.chat.id, 
                                             message.reply_to_message.from_user.id
                                            )
    if user.is_chat_admin():
        return

    f_name = message.reply_to_message.from_user.first_name
    l_name = message.reply_to_message.from_user.last_name
    username = message.reply_to_message.from_user.username
    if l_name == None:
        await message.answer(f"Пользователь {f_name} (@{username}) разбанен")
    else:
        await message.answer(f"Пользователь {f_name} {l_name} (@{username}) разбанен")
    await message.bot.delete_message(message.chat.id, message.message_id)  # remove admin message
    await message.bot.unban_chat_member(chat_id=message.chat.id, 
                                        user_id=message.reply_to_message.from_user.id
                                       )

@dp.message_handler(is_admin=True, commands="mute", commands_prefix="!")
async def cmd_readonly(message: types.Message):
   
    # Check if command is sent as reply to some message
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение")
        return

    # Admins cannot be restricted
    user = await message.bot.get_chat_member(message.chat.id, 
                                             message.reply_to_message.from_user.id
                                            )
    if user.is_chat_admin():
        await message.reply("Нельзя замьютить администратора!")
        return

    words = message.text.split()
    restriction_time: int = 0
    if len(words) > 1:  # !mute with arg
        restriction_time = utils.get_restriction_time(words[1])
        if not restriction_time:
            await message.reply("Неправильный формат времени!\nИспользуйте число + символ m, h или d.\nНапример: <code>!mute 7d</code>", parse_mode = 'HTML' )
            return
    else:
    	restriction_time = 86400 * 367

    await message.bot.restrict_chat_member(message.chat.id,
                                           message.reply_to_message.from_user.id,
                                           types.ChatPermissions(),
                                           until_date=int(time()) + restriction_time
                                           )
    
    f_name = message.reply_to_message.from_user.first_name
    l_name = message.reply_to_message.from_user.last_name
    username = message.reply_to_message.from_user.username
    if len(words) > 1:
        if l_name == None:
            await message.answer(f"Пользователю {f_name} (@{username}) выдан мут на " + (
                                 "({restriction_time})").format(restriction_time=words[1])
                                )
        else:
            await message.answer(f"Пользователю {f_name} {l_name} (@{username}) выдан мут на " + (
                                 "({restriction_time})").format(restriction_time=words[1])
                                )
    else:
        if l_name == None:
            await message.answer(f"Пользователю {f_name} (@{username}) выдан мут навсегда")
        else:
            await message.answer(f"Пользователю {f_name} {l_name} (@{username}) выдан мут навсегда")
    await message.bot.delete_message(message.chat.id, message.message_id)# remove admin message

@dp.message_handler(is_admin=True, commands="unmute", commands_prefix="!")
async def cmd_unreadonly(message: types.Message):
    
    # Check if command is sent as reply to some message
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение")
        return

    user = await message.bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    if user.is_chat_admin():
        await message.reply("Нельзя замьютить администратора!")
        return

    await message.bot.restrict_chat_member(message.chat.id,
                                           message.reply_to_message.from_user.id,
                                           types.ChatPermissions(
                                               can_send_messages=True,
                                               can_send_media_messages=True,
                                               can_send_polls=True,
                                               can_send_other_messages=True,
                                               can_add_web_page_previews=True,
                                               can_change_info=True,
                                               can_invite_users=True,
                                               can_pin_messages=True)
                                          )
    
    f_name = message.reply_to_message.from_user.first_name
    l_name = message.reply_to_message.from_user.last_name
    username = message.reply_to_message.from_user.username
    if l_name == None:
        await message.answer(f"Пользователь {f_name} (@{username}) размучен")
    else:
        await message.answer(f"Пользователь {f_name} {l_name} (@{username}) размучен")
    await message.bot.delete_message(message.chat.id, message.message_id)# remove admin message
    
@dp.message_handler(content_types=["any"])
async def ban_anon_channel(message: types.Message):
    if message.from_user.first_name == "Channel" and message.sender_chat.id not in config.channel_whitelist:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
