# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import json

from src.telegram.bot_core import BotDB
from src.telegram.logger._logger import logger_msg


async def delete_friends_sql(user_id: int, friend_id: int):
    friends_user = BotDB.get_friends_by_user(user_id)

    if str(friends_user) == 'False':
        return False

    if not friends_user:
        return False

    friend_id = int(friend_id)

    friends_user = json.loads(friends_user)

    if friend_id not in friends_user:
        return '-1'

    try:
        friends_user.remove(friend_id)
    except Exception as es:
        error_msg = f'Не могу удалить друга из списка из sql "{user_id}" "{friends_user}" "{es}"'

        logger_msg(error_msg)

        return False

    res = BotDB.edit_user('friends', friends_user, user_id)

    return res
