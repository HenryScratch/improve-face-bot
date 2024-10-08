# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from aiogram import types

from src.telegram.bot_core import bot
from src.telegram.logger._logger import logger_msg


async def _send_group_by_user(id_user, file_list, _text_msg):
    media = types.MediaGroup()

    for count, file in enumerate(file_list):

        if 'pic_' in file:
            if count > 0:
                _msg = None
            else:
                _msg = _text_msg

            media.attach_photo(types.InputFile(file), _msg)

        if 'vid_' in file:
            if count > 0:
                _msg = None
            else:
                _msg = _text_msg

            media.attach_video(types.InputFile(file), _msg)

    try:
        msg = await bot.send_media_group(id_user, media=media)
    except Exception as es:
        error_ = f'Ошибка при отправке медиагруппы голосования "{id_user}" {es}'

        logger_msg(error_)

        return False

    return msg
