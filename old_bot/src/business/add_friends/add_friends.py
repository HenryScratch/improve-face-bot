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

from src.business.add_friends._add_friends_sql import add_friends_sql
from src.business.logic.write_chat import write_chat
from src.telegram.keyboard.keyboards import Admin_keyb
from src.telegram.logger._logger import logger_msg
from src.telegram.sendler.sendler import Sendler_msg


async def add_friends(message: Message, state: FSMContext):
    await write_chat(message)

    await state.finish()

    user_id = message.chat.id

    try:
        friend_id = message.user_shared.user_id
    except Exception as es:
        error_user = f'Ошибка при разборе контакта. Попробуйте другой контакт'

        error_admin = f"У пользователя ошибка при распознавания контакта '{user_id}' '{es}'"

        logger_msg(error_admin)

        await Sendler_msg.sendler_to_admin(message, error_admin, None)

        await Sendler_msg.send_msg_message(message, error_user, None)

        return False

    res_add = await add_friends_sql(user_id, friend_id)

    bot_link = await message.bot.me

    bot_link = f"https://t.me/{bot_link.username}"

    _msg = f'✅ Успешно добавил друга с ID "{friend_id}"\n\n' \
           f'⚠️ Обязательно отправьте другу ссылку, что бы он зашёл в бота <a href="{bot_link}">{bot_link}</a>' if \
        res_add else f'❌ Не смог добавить друга с ID "{friend_id}"'

    if res_add == '-1':
        _msg = f'🔸 Друг с ID "{friend_id}" уже был добавлен ранее'

    keyb = None

    await Sendler_msg.send_msg_message(message, _msg, keyb)

    # Взаимное добавление друга, т.е. моему другу добавляем меня в друзья
    res_end_to_end_add = await add_friends_sql(friend_id, user_id)

    return True
