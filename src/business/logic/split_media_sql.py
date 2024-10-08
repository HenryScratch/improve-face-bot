# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from src.telegram.logger._logger import logger_msg


async def split_media_sql(_patch_file):
    try:
        file_list = _patch_file.split(';')
    except Exception as es:
        error_ = f'Ошибка распарсинга файлов из медиагруппы "{_patch_file}" "{es}"'

        logger_msg(error_)

        return False

    return file_list
