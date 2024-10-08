# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import json


async def search_answer(poll_data, id_user, answer):
    id_pk_poll = poll_data[0]

    send_users = poll_data[1]

    results = poll_data[2]

    send_users = json.loads(send_users)

    results = json.loads(results)

    for count, row in enumerate(send_users):
        id_user_sql = row['id']

        message_id_sql = row['message_id']

        answer_sql = row['answer']

        if id_user_sql == id_user:

            if answer == '-1':
                old_answer = send_users[count]['answer']

                results[str(old_answer)] -= 1

                send_users[count]['answer'] = None
            else:
                send_users[count]['answer'] = answer

    if answer != '-1':
        results[str(answer)] += 1

    return_dict = {"id_pk_poll": id_pk_poll, "send_users": send_users, "results": results}

    return return_dict
