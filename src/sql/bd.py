import datetime
import sqlite3
from datetime import datetime

from src.telegram.logger._logger import logger_msg


class BotDB:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __init__(self, db_file):
        try:

            self.conn = sqlite3.connect(db_file, timeout=30)
            print('Подключился к SQL DB:', db_file)
            self.cursor = self.conn.cursor()
            self.check_table()
        except Exception as es:
            print(f'Ошибка при работе с SQL {es}')

    def check_table(self):

        try:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS "
                                f"users (id_pk INTEGER PRIMARY KEY AUTOINCREMENT, "
                                f"id_user TEXT, "
                                f"login TEXT, "
                                f"friends TEXT DEFAULT [], "
                                f"status TEXT DEFAULT new, "
                                f"join_date DATETIME, "
                                f"last_time DATETIME DEFAULT 0, "
                                f"license BOOLEAN DEFAULT 0, "
                                f"date_buy DATETIME DEFAULT 0, "
                                f"other TEXT)")

        except Exception as es:
            logger_msg(f'SQL исключение check_table users {es}')

            return False

        try:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS "
                                f"down_media (id_pk INTEGER PRIMARY KEY AUTOINCREMENT, "
                                f"id_user TEXT, "
                                f"media_type TEXT, "
                                f"text TEXT, "
                                f"media_file TEXT, "
                                f"link TEXT, "
                                f"other TEXT)")

        except Exception as es:
            print(f'SQL исключение down_media {es}')

        try:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS "
                                f"polls (id_pk INTEGER PRIMARY KEY AUTOINCREMENT, "
                                f"owner_id_chat TEXT, "
                                f"owner_poll_id TEXT, "
                                f"ids_polls TEXT, "  # По ним буду искать какой голосование редактировать
                                f"send_users TEXT, "  # Список id_message кому выслал
                                f"results TEXT, "  # Эти результаты обновлять и рассылать
                                f"other TEXT)")

        except Exception as es:
            print(f'SQL исключение polls {es}')

        return True

    def check_or_add_user(self, id_user, login):

        login = ''  # Не сохраняем логин

        result = self.cursor.execute(f"SELECT * FROM users WHERE id_user='{id_user}'")

        response = result.fetchall()

        if not response:
            now_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            self.cursor.execute("INSERT OR IGNORE INTO users ('id_user', 'login',"
                                "'join_date') VALUES (?,?,?)",
                                (id_user, login,
                                 now_date,))

            self.conn.commit()

            return True

        return False

    def get_friends_by_user(self, id_user):
        try:
            result = self.cursor.execute(f"SELECT friends FROM users "
                                         f"WHERE id_user = '{id_user}'")

            response = result.fetchall()[0][0]
        except Exception as es:
            logger_msg(f'SQL: Не могу получить список друзей у пользователя "{id_user}" "{es}"')

            return False

        return response

    def edit_user(self, key, value, id_user):

        try:

            result = self.cursor.execute(f"SELECT {key} FROM users "
                                         f"WHERE id_user = '{id_user}'")

            response = result.fetchall()

            if not response:
                logger_msg(f'SQL Не могу отредактировать пользователя "{id_user}" поле: "{key}" значение: "{value}"')
                return False

            self.cursor.execute(f"UPDATE users SET {key} = '{value}' WHERE id_user = '{id_user}'")

            self.conn.commit()

            print(f'SQL: Отредактировал пользователя "{id_user}" поле: "{key}" значение: "{value}"')

            return True

        except Exception as es:
            logger_msg(f'SQL ERROR: Не смог изменить пользователя"{id_user}" поле: "{key}" значение: "{value}" "{es}"')

            return False

    def add_media_group_ads_post(self, id_user, _type_msg, _text_response, _sql_file_patch):

        result = self.cursor.execute(f"SELECT * FROM down_media WHERE id_user='{id_user}'")

        response = result.fetchall()

        if not response:

            self.cursor.execute("INSERT OR IGNORE INTO down_media ('id_user', 'media_type',"
                                "'text', 'media_file') VALUES (?,?,?,?)",
                                (id_user, _type_msg,
                                 _text_response, _sql_file_patch))

            self.conn.commit()

            id_pk = self.cursor.lastrowid
        else:

            check_media_group = self.cursor.execute(f"SELECT * FROM down_media WHERE media_type='{_type_msg}'")

            response_media_group = check_media_group.fetchall()

            if not response_media_group:
                # Нет еще такой медиагруппы

                self.cursor.execute(f"UPDATE down_media SET media_type = '{_type_msg}', "
                                    f"text = '{_text_response}', media_file = '{_sql_file_patch}'"
                                    f" WHERE id_user = '{id_user}'")

                self.conn.commit()

                id_pk = response[0][0]
            else:
                # есть файлы от медиагруппы

                id_pk = response_media_group[0][0]

                sql_text = response_media_group[0][3]

                sql_path_file = response_media_group[0][4]

                if sql_path_file == _sql_file_patch:
                    return id_pk

                new_text = _text_response if _text_response else sql_text

                file_patch = f'{sql_path_file};{_sql_file_patch}'

                self.cursor.execute(f"UPDATE down_media SET media_type = '{_type_msg}', "
                                    f"text = '{new_text}', media_file = '{file_patch}'"
                                    f" WHERE id_user = '{id_user}'")

                self.conn.commit()

        return id_pk

    def get_media_poll(self, id_pk):

        result = self.cursor.execute(f"SELECT * FROM down_media WHERE id_pk='{id_pk}'")

        response = result.fetchall()

        try:

            response = response[0]
        except:
            return False

        return response

    def update_poll_send_friend(self, owner_poll_id, ids_polls, send_users):
        import json

        try:
            ids_polls = json.dumps(ids_polls)

            send_users = json.dumps(send_users)

            self.cursor.execute(f"UPDATE polls SET ids_polls = '{ids_polls}', "
                                f"send_users = '{send_users}' WHERE owner_poll_id = '{owner_poll_id}'")

            self.conn.commit()

        except Exception as es:
            error_ = f'SQL ошибка: не обновить poll "{owner_poll_id}" "{es}"'

            logger_msg(error_)

            return False

        return True

    def create_poll(self, id_user, owner_poll_id, ids_polls, send_users, results_answer):
        import json

        ids_polls = json.dumps(ids_polls)

        send_users = json.dumps(send_users)

        results_answer = json.dumps(results_answer)

        try:
            self.cursor.execute("INSERT OR IGNORE INTO polls ('owner_id_chat', 'owner_poll_id',"
                                "'ids_polls', 'send_users', 'results') VALUES (?,?,?,?,?)",
                                (id_user, owner_poll_id, ids_polls, send_users, results_answer))

            self.conn.commit()

        except Exception as es:
            error_ = f'SQL ошибка: не могу создать poll "{es}"'

            logger_msg(error_)

            return False

        return True

    def get_poll_by_ids_polls(self, id_poll):
        """Ищу голосование по IDшникам голосований пользователей"""
        try:
            result = self.cursor.execute(f"SELECT id_pk, send_users, results FROM polls "
                                         f"WHERE ids_polls LIKE '%{id_poll}%'")

            response = result.fetchall()[0]
        except Exception as es:
            logger_msg(f'SQL: Не могу получить голосование id "{id_poll}" "{es}"')

            return False

        return response

    def update_answer_poll(self, id_pk, send_users, results):
        import json

        try:
            send_users = json.dumps(send_users)

            results = json.dumps(results)

            self.cursor.execute(f"UPDATE polls SET send_users = '{send_users}', "
                                f"results = '{results}' WHERE id_pk = '{id_pk}'")

            self.conn.commit()

        except Exception as es:
            error_ = f'SQL ошибка: не обновить update_answer_poll "{id_pk}" "{es}"'

            logger_msg(error_)

            return False

        return True

    def count_all_users(self):

        try:
            result = self.cursor.execute(f"SELECT COUNT(*) FROM users")

            response = result.fetchall()

        except Exception as es:
            logger_msg(f'SQL ошибка! При count_all_users "{es}"')

            return False

        try:
            response = response[0][0]
        except Exception as es:
            print(f'Ошибка SQL count_all_users parsing {es}')

            return False

        return response

    def count_all_poll(self):

        try:
            result = self.cursor.execute(f"SELECT COUNT(*) FROM polls")

            response = result.fetchall()

        except Exception as es:
            logger_msg(f'SQL ошибка! При count_all_poll "{es}"')

            return False

        try:
            response = response[0][0]
        except Exception as es:
            print(f'Ошибка SQL count_all_poll parsing {es}')

            return False

        return response

    def close(self):

        self.conn.close()

        logger_msg('Отключился от SQL BD')
