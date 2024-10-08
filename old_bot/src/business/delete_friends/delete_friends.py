# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from src.business.delete_friends._delete_friends_sql import delete_friends_sql
from src.business.logic.write_chat import write_chat
from src.telegram.keyboard.keyboards import Admin_keyb
from src.telegram.logger._logger import logger_msg
from src.telegram.sendler.sendler import Sendler_msg


async def delete_friends(message: Message, state: FSMContext):
    await write_chat(message)

    await state.finish()

    user_id = message.chat.id

    try:
        await message.bot.delete_message(user_id, message.message_id)
    except:
        pass

    try:
        _, friend_id = str(message.text).split('_')
    except Exception as es:
        error_user = f'❌ Не смог удалить друга'

        error_admin = f"Ошибка при разборе для удаления call delete_friends {es} '{user_id}' '{es}'"

        logger_msg(error_admin)

        await Sendler_msg.sendler_to_admin(message, error_admin, None)

        await Sendler_msg.send_msg_message(message, error_user, None)

        return False

    if 'chat' in friend_id:
        friend_id = -int(friend_id[4:])

    res_del = await delete_friends_sql(user_id, friend_id)

    _msg = f'🗑 Успешно удалил друга с ID "{friend_id}"' if res_del else \
        f'❌ Не смог удалить друга с ID "{friend_id}"'

    if res_del == '-1':
        _msg = f'🔸 Друг с ID "{friend_id}" уже был удалён ранее'

    keyb = None

    await Sendler_msg.send_msg_message(message, _msg, keyb)

    return True
