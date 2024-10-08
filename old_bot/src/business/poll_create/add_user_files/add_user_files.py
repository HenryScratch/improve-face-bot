# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from aiogram.types import Message

from src.business.poll_create.add_user_files.download_photo import download_photo_
from src.telegram.sendler.sendler import Sendler_msg
from src.telegram.bot_core import BotDB


async def no_media_group(message: Message):
    id_user = message.chat.id

    try:

        _text_response = message.caption if message.caption is not None else message.text

        _sql_file_patch = await download_photo_(message)

        id_pk = BotDB.add_media_ads_post('media', 'photo', _text_response, _sql_file_patch)

        return id_pk

    except Exception as es:
        _error = f'Не смог отправить  {id_user} на шаге добавления материала в ' \
                 f'базу. Причина: {es}'

        print(f'{_error}\n')

        await Sendler_msg.sendler_to_admin_mute(message, _error, None)

        return False


async def go_media_group(message: Message):
    id_user = message.chat.id

    id_media_group = message.media_group_id

    _text_response = message.caption if message.caption else ''

    _sql_file_patch = await download_photo_(message)

    id_pk = BotDB.add_media_group_ads_post(id_user, f'media_group-{id_media_group}', _text_response, _sql_file_patch)

    return id_pk


async def add_user_files(message: Message):
    id_user = message.chat.id

    if message.media_group_id:
        id_pk = await go_media_group(message)

    else:
        id_pk = await no_media_group(message)

    return id_pk
