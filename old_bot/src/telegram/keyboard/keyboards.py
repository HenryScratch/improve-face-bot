from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from settings import COUNT_ANSWER_FROM_QUESTIONS, ADMIN
from src.business.logic.fix_percent import fix_percent


class Admin_keyb:
    my_friends_btn = f'👥 Мои друзья'

    poll_btn = f'➕ Создать голосование'

    def start_keyb(self, id_user):
        start_keyb = ReplyKeyboardMarkup()

        start_keyb.add(KeyboardButton('👋 Добавить друга', request_user=types.KeyboardButtonRequestUser(request_id=1)))

        if str(id_user) in ADMIN:
            start_keyb.add(KeyboardButton('admin'))

        return start_keyb

    def result_poll(self):
        self._start_key = InlineKeyboardMarkup(row_width=2)

        self._start_key.add(InlineKeyboardButton(text=f'Проголосовали мои друзья 👇', callback_data=f'mok'))

        self._start_key.add(InlineKeyboardButton(text=f'0% (0)', callback_data=f'mok'))

        for count in range(COUNT_ANSWER_FROM_QUESTIONS - 1):
            self._start_key.insert(InlineKeyboardButton(text=f'0% (0)', callback_data=f'mok'))

        return self._start_key

    def update_answer(self, results):
        self._start_key = InlineKeyboardMarkup(row_width=2)

        self._start_key.add(InlineKeyboardButton(text=f'Проголосовали мои друзья 👇', callback_data=f'mok'))

        count_keyb = 0

        total_voice = 0

        for key, value in results.items():
            total_voice += value

        for key, value in results.items():
            try:
                text = round(value / (total_voice / 100), 2)

                text = fix_percent(text)
            except ZeroDivisionError:
                text = 0

            text_button = f"{text}% ({value})"

            if count_keyb == 0:
                self._start_key.add(InlineKeyboardButton(text=text_button, callback_data=f'mok'))
            else:
                self._start_key.insert(InlineKeyboardButton(text=text_button, callback_data=f'mok'))

            count_keyb += 1

        return self._start_key
