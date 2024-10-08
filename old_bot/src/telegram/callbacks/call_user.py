from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from src.telegram.sendler.sendler import *

from src.telegram.keyboard.keyboards import *


async def mok(call: types.CallbackQuery, state: FSMContext):
    await call.answer(f'Что бы проголосовать, выберите вариант в самом голосование, выше☝️\n\n'
                      f'Здесь отображаются результаты', show_alert=True)

    await Sendler_msg.log_client_call(call)

    return True


def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(mok, text='mok', state='*')
