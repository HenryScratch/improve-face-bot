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


async def add_friends_sql(user_id: int, friend_id: int):
    new_user = BotDB.check_or_add_user(user_id, '')

    friends_user = BotDB.get_friends_by_user(user_id)

    if str(friends_user) == 'False':
        return False

    if not friends_user:
        friends_user = []
    else:
        friends_user = json.loads(friends_user)

    if friend_id not in friends_user:
        friends_user.append(friend_id)

        res = BotDB.edit_user('friends', friends_user, user_id)

        return res
    else:
        # Уже был в друзьях
        return '-1'
