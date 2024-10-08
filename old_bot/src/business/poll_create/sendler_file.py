# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from settings import TITLE_QUESTION
from src.business.logic.pinned_msg import pinned_msg
from src.business.logic.split_media_sql import split_media_sql
from src.business.logic.write_chat import new_writer_chat
from src.business.poll_create.send_media_poll._send_from_friends import _send_from_friends
from src.business.poll_create.send_media_poll._send_group_by_user import _send_group_by_user
from src.business.poll_create.send_poll.send_pol_by_user import send_pol_by_user
from src.telegram.bot_core import bot
from src.telegram.logger._logger import logger_msg


class SenderFile:

    @staticmethod
    async def sender_media_group(id_user, _patch_file, _text_msg):

        file_list = await split_media_sql(_patch_file)

        if not file_list:
            return False

        owner_media_msg = await _send_group_by_user(id_user, file_list, _text_msg)

        count_answer = len(file_list)

        await new_writer_chat(id_user)

        owner_poll_msg = await send_pol_by_user(id_user, count_answer, TITLE_QUESTION)

        await pinned_msg(id_user, owner_poll_msg)

        await new_writer_chat(id_user)

        res_send_friends = await _send_from_friends(id_user, count_answer, file_list, _text_msg, owner_poll_msg)

        return res_send_friends

    @staticmethod
    async def sender_text(id_user, _text_msg, keyb=None):
        try:
            await bot.send_message(id_user, _text_msg, reply_markup=keyb)
        except Exception as es:

            error_ = f'Ошибка sender_text {es}'

            logger_msg(error_)

            return False

        return True
