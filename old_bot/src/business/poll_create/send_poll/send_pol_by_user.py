# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from settings import TITLE_QUESTION
from src.telegram.bot_core import bot
from src.telegram.keyboard.keyboards import Admin_keyb
from src.telegram.logger._logger import logger_msg


async def send_pol_by_user(id_user, count_answer, text_pol=False):
    answer_list = [f'Вариант {x + 1}' for x in range(count_answer)]

    title_poll = text_pol if text_pol else TITLE_QUESTION

    try:
        poll = await bot.send_poll(id_user, question=title_poll, options=answer_list,
                                   is_anonymous=False, reply_markup=Admin_keyb().result_poll(),
                                   protect_content=True)
    except Exception as es:
        error_msg = f'Ошибка при отправке голосования пользователю "{id_user}" причина: "{es}"'

        logger_msg(error_msg)

        return False

    return poll
