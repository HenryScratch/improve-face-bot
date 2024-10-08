# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from src.telegram.bot_core import bot
from src.telegram.keyboard.keyboards import Admin_keyb
from src.telegram.logger._logger import logger_msg


async def updater_answer_from_users(send_users, results):
    keyb = Admin_keyb().update_answer(results)

    for row in send_users:
        id_user_sql = row['id']

        message_id_sql = row['message_id']

        try:
            await bot.edit_message_reply_markup(id_user_sql, message_id_sql, reply_markup=keyb)
        except Exception as es:
            error_ = f'Не могу обновить результаты голосования у пользователя "{id_user_sql}" "{es}"'

            logger_msg(error_)

            continue

        print(f'Успешно обновил результаты у "{id_user_sql}"')

    return True
