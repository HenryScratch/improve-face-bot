# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from aiogram import types


async def create_media_group_user(file_list, _text_msg):
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

    return media
