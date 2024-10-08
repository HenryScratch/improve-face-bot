# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from aiogram.types import ChatActions, Message
from src.telegram.bot_core import bot


async def write_chat(message: Message):
    try:
        await message.bot.send_chat_action(message.chat.id, ChatActions.TYPING)
    except:
        pass


async def new_writer_chat(id_chat):
    try:
        await bot.send_chat_action(id_chat, ChatActions.TYPING)
    except:
        pass
