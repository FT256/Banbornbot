from time import time

from aiogram import types
from dispatcher import dp, bot

import utils

@dp.message_handler(is_admin=True, commands=['ban'], commands_prefix="!/")
async def cmd_ban(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение")
        return

    user = await message.bot.get_chat_member(message.chat.id,
                                             message.reply_to_message.from_user.id)

    if message.reply_to_message.from_user.id == message.from_user.id:
        await message.reply("Нельзя забанить самого себя =)")
        return

    if user.is_chat_admin():
        await message.reply("Нельзя изменять права администраторов")
        return

    user = message.reply_to_message.from_user
    if user.last_name is not None:
        await message.answer(f"Пользователь {user.first_name} {user.last_name} (@{user.username}) забанен навсегда!")
    else:
        await message.answer(f"Пользователь {user.first_name} (@{user.username}) забанен навсегда!")
    await message.bot.delete_message(message.chat.id, message.message_id)  # remove admin message
    await message.bot.kick_chat_member(chat_id=message.chat.id,
                                       user_id=message.reply_to_message.from_user.id
                                       )


@dp.message_handler(is_admin=True, commands=["unban"], commands_prefix="!/")
async def cmd_unban(message: types.Message):
    # Check if command is sent as reply to some message
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение")
        return

    user = await message.bot.get_chat_member(message.chat.id,
                                             message.reply_to_message.from_user.id
                                             )
    if user.is_chat_admin():
        await message.reply("Нельзя изменять права администраторов")
        return

    user = message.reply_to_message.from_user
    if user.last_name is not None:
        await message.answer(f"Пользователь {user.first_name} {user.last_name} (@{user.username}) разбанен")
    else:
        await message.answer(f"Пользователь {user.first_name} (@{user.username}) разбанен")
    await message.bot.delete_message(message.chat.id, message.message_id)  # remove admin message
    await message.bot.unban_chat_member(chat_id=message.chat.id,
                                        user_id=message.reply_to_message.from_user.id
                                        )


@dp.message_handler(is_admin=True, commands="mute", commands_prefix="!/")
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
        await message.reply("Нельзя изменять права администраторов")
        return

    words = message.text.split()
    if len(words) > 1:  # !mute with arg
        restriction_time = utils.get_restriction_time(words[1])
        if not restriction_time:
            await message.reply(
                "Неправильный формат времени!\nИспользуйте число + символ m, h или d.\nНапример: <code>!mute 7d</code>"
            )
            return
    else:
        restriction_time = 86400 * 367

    await message.bot.restrict_chat_member(message.chat.id,
                                           message.reply_to_message.from_user.id,
                                           types.ChatPermissions(),
                                           until_date=int(time()) + restriction_time
                                           )

    user = message.reply_to_message.from_user
    if len(words) > 1:
        if user.last_name is not None:
            await message.answer(f"Пользователю {user.first_name} {user.last_name} (@{user.username}) выдан мут на " + (
                "({restriction_time})").format(restriction_time=restriction_time_to_human_readable(restriction_time))
                                 )
        else:
            await message.answer(f"Пользователю {user.first_name} (@{user.username}) выдан мут на " + (
                "({restriction_time})").format(restriction_time=restriction_time_to_human_readable(restriction_time))
                                 )
    else:
        if user.last_name is not None:
            await message.answer(
                f"Пользователю {user.first_name} {user.last_name} (@{user.username}) выдан мут навсегда")
        else:
            await message.answer(f"Пользователю {user.first_name} (@{user.username}) выдан мут навсегда")
    await message.bot.delete_message(message.chat.id, message.message_id)  # remove admin message


@dp.message_handler(is_admin=True, commands="unmute", commands_prefix="!/")
async def cmd_unreadonly(message: types.Message):
    # Check if command is sent as reply to some message
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение")
        return

    user = await message.bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    if user.is_chat_admin():
        await message.reply("Нельзя изменять права администраторов!")
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

    user = message.reply_to_message.from_user
    if user.last_name is not None:
        await message.answer(f"Пользователь {user.first_name} {user.last_name} (@{user.username}) размучен")
    else:
        await message.answer(f"Пользователь {user.first_name} (@{user.username}) размучен")
    await message.bot.delete_message(message.chat.id, message.message_id)  # remove admin message

@dp.message_handler(is_admin=True, commands=['id'], commands_prefix="!/")
async def cmd_get_userid(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение")
        return

    await message.reply(message.reply_to_message.from_user.id)
        
    await message.bot.delete_message(message.chat.id, message.message_id)  # remove admin message
    
