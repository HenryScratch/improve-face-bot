# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import json

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from src.business.logic.write_chat import write_chat
from src.telegram.bot_core import BotDB
from src.telegram.keyboard.keyboards import Admin_keyb
from src.telegram.sendler.sendler import Sendler_msg


async def formate_friends_list(friends_user):
    msg = ''

    for count, user in enumerate(json.loads(friends_user)):
        text_user = f"chat{str(user)[1:]}" if '-' in str(user) else user

        msg += f'{count + 1}. {user} Удалить /del_{text_user}\n'

    return msg


async def my_friends(message: Message, state: FSMContext):
    await write_chat(message)

    await state.finish()

    user_id = message.chat.id

    try:
        await message.bot.delete_message(user_id, message.message_id)
    except:
        pass

    friends_user = BotDB.get_friends_by_user(user_id)

    msg = '<b>Список друзей</b>\n\n'

    if not friends_user or str(friends_user) == '[]':
        msg = '⭕️ Список друзей пуст'
    else:
        msg += await formate_friends_list(friends_user)

    keyb = None

    await Sendler_msg.send_msg_message(message, msg, keyb)

    return True
