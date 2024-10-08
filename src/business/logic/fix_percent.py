# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from src.telegram.logger._logger import logger_msg


def fix_percent(value):
    try:
        _value = str(value).split('.')

        lens = len(_value[-1])

        if lens == 1:
            value = str(value)[:-2]

    except Exception as es:
        logger_msg(f'Не могу обработать проценты "{es}"')

    return value
