# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from src.telegram.logger._logger import logger_msg
from src.telegram.bot_core import bot


async def pinned_msg(id_user, target_message):
    try:
        await bot.pin_chat_message(chat_id=int(id_user),
                                   message_id=target_message['message_id'])
    except Exception as es:
        logger_msg(f'Не могу запинить сообщение "{es}" user "{id_user}"')

        return False

    return True
