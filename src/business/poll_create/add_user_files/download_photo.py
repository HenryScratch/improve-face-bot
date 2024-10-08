# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import os
import random
from datetime import datetime

from aiogram.types import Message

from settings import media_path


async def download_photo_(message: Message):
    try:
        file_id = message.photo[-1].file_id

        file = await message.bot.get_file(file_id)

        file_path = file.file_path

        _sql_file_patch = os.path.join(media_path,
                                       f'pic_{datetime.now().strftime("%H%M%S")}{random.randint(1, 100)}.jpg')

        await message.bot.download_file(file_path, _sql_file_patch)

        return _sql_file_patch
    except Exception as es:
        print(f'Ошибка при скачивание фото "{es}"')

        return False
