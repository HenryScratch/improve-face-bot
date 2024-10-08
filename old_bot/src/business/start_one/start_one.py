# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import asyncio

from settings import START_MESSAGE
from src.business.logic.write_chat import write_chat
from src.telegram.keyboard.keyboards import Admin_keyb

from src.telegram.sendler.sendler import Sendler_msg

from aiogram.types import Message, ChatActions

from src.telegram.bot_core import BotDB

from aiogram.dispatcher import FSMContext


async def start_one(message: Message, state: FSMContext):
    await state.finish()

    await Sendler_msg.log_client_message(message)

    await write_chat(message)

    id_user = message.chat.id

    login = message.chat.username

    new_user = BotDB.check_or_add_user(id_user, login)

    keyb = None

    await Sendler_msg.send_msg_message(message, START_MESSAGE, keyb)

    return True
