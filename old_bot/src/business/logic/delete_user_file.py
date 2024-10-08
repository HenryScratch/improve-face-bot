# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import os


async def delete_file(files_list):
    for file in files_list:
        try:
            os.remove(file)
        except:
            continue

    return True
