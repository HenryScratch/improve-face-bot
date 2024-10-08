# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from src.business.poll_create.sendler_file import SenderFile
from src.telegram.logger._logger import logger_msg


async def send_media_poll(id_user, row_sql_response):
    try:

        _, __, _type_msg, _text_msg, _patch_file, *_ = row_sql_response

    except Exception as es:
        _error_user = f'⭕️ К сожалению не смог отправить медиафайлы присланные вами'

        _error = f'Не смог отправить медиа файлы от голосования пользователя "{id_user}" Причина: "{es}"'

        logger_msg(f'{_error}\n')

        await SenderFile.sender_text(id_user, _error_user)

        return False

    # Отправляю

    res_ = await SenderFile.sender_media_group(id_user, _patch_file, _text_msg)

    return res_
