# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import json

from src.business.logic.write_chat import new_writer_chat
from src.business.poll_create.send_media_poll._send_group_by_user import _send_group_by_user
from src.business.poll_create.send_poll.send_pol_by_user import send_pol_by_user
from src.telegram.bot_core import BotDB
from src.telegram.bot_core import bot
from src.telegram.keyboard.keyboards import Admin_keyb
from src.telegram.logger._logger import logger_msg


async def _send_from_friends(id_user, count_answer, file_list, _text_msg, owner_poll_msg):
    friends_user = BotDB.get_friends_by_user(id_user)

    friends_user = json.loads(friends_user)

    owner_poll_id = owner_poll_msg.poll.id

    owner_msg_id = owner_poll_msg.message_id

    send_users = [{'id': id_user, "message_id": owner_msg_id, "answer": None}]

    ids_polls = [owner_poll_id]

    results_answer = {x: 0 for x in range(count_answer)}

    res_create_poll_sql = BotDB.create_poll(id_user, owner_poll_id, ids_polls, send_users, results_answer)

    keyb = Admin_keyb().result_poll()

    for friend in friends_user:

        await new_writer_chat(id_user)

        res_send_media = await _send_group_by_user(friend, file_list, _text_msg)

        if not res_send_media and '-' in str(friend):
            chat_no_rules = f'⚠️ Нет доступа к написанию сообщений в чат <b>"{friend}"</b>\n\n' \
                            f'Добавьте бота в чат что бы он получил права писать сообщения в чат'

            try:
                await bot.send_message(id_user, chat_no_rules, reply_markup=keyb)
            except Exception as es:
                logger_msg(f'Не могу оповестить owner о том что у бота нет прав писать в чат "{id_user}" '
                           f'"{friend}" "{es}"')

            continue

        if not res_send_media:
            continue

        friend_poll_msg = await send_pol_by_user(friend, count_answer)

        if not friend_poll_msg:
            continue

        friends_poll_id = friend_poll_msg.poll.id

        friends_message_id = friend_poll_msg.message_id

        send_users.append({'id': friend, "message_id": friends_message_id, "answer": None})

        ids_polls.append(friends_poll_id)

        res_create_poll_sql = BotDB.update_poll_send_friend(owner_poll_id, ids_polls, send_users)

        continue

    print(f'Закончил рассылку голосований всем друзья пользователя "{id_user}"')

    return True
