from aiogram.dispatcher import FSMContext
from aiogram.types import Message, PollAnswer

from aiogram import Dispatcher, types

from settings import TITLE_QUESTION, COUNT_ANSWER_FROM_QUESTIONS, START_QUESTION, ADMIN, scr_friend
from src.business.add_chat.add_chat import add_chat
from src.business.add_friends.add_friends import add_friends
from src.business.answer_job.search_answer.search_answer import search_answer
from src.business.answer_job.updater_answer_from_users.updater_answer_from_users import updater_answer_from_users
from src.business.delete_friends.delete_friends import delete_friends
from src.business.start_one.start_one import start_one
from src.business.my_friends.my_friends import my_friends
from src.telegram.keyboard.keyboards import Admin_keyb
from src.telegram.logger._logger import logger_msg
from src.telegram.sendler.sendler import Sendler_msg
from src.telegram.state.states import States, start_question

from src.telegram.bot_core import BotDB


async def start(message: Message, state: FSMContext):
    await state.finish()

    result = await start_one(message, state)

    return result


async def _add_friends(message: Message, state: FSMContext):
    return await add_friends(message, state)


async def _add_chat(message: Message, state: FSMContext):
    return await add_chat(message, state)


async def _my_friends(message: Message, state: FSMContext):
    return await my_friends(message, state)


async def _delete_friends(message: Message, state: FSMContext):
    return await delete_friends(message, state)


async def _create_poll(message: Message, state: FSMContext):
    await state.finish()

    await Sendler_msg.log_client_message(message)

    id_user = message.chat.id

    friends_user = BotDB.get_friends_by_user(id_user)

    if not friends_user or str(friends_user) == '[]':
        msg = f'⚠️ Вы не добавили ни одного друга. Что бы создавать голосования, пожалуйста, добавьте друзей!'

        await Sendler_msg.send_msg_message(message, msg, Admin_keyb().result_poll())

        await state.finish()

        return False

    await Sendler_msg.send_msg_message(message, START_QUESTION, None)

    await States.start_question.set()

    return True


async def req_poll(poll: PollAnswer):
    id_poll = poll.poll_id

    id_user = poll.values['user'].id

    if not poll.values["option_ids"]:
        answer = '-1'
    else:
        answer = poll.values["option_ids"][0]

    poll_data = BotDB.get_poll_by_ids_polls(id_poll)

    if not poll_data:
        error = f'Не могу найти голосование в sql базе "{id_poll}"'

        logger_msg(error)

        return True

    answer_dict = await search_answer(poll_data, id_user, answer)

    BotDB.update_answer_poll(answer_dict['id_pk_poll'], answer_dict['send_users'], answer_dict['results'])

    res_update = await updater_answer_from_users(answer_dict['send_users'], answer_dict['results'])

    return res_update


async def admin(message: Message, state: FSMContext):
    await Sendler_msg.log_client_message(message)

    id_user = message.chat.id

    if str(id_user) not in ADMIN:
        return False

    await state.finish()

    count_users = BotDB.count_all_users()

    count_polls = BotDB.count_all_poll()

    msg = f'🔰 <b>Статистика:</b>\n\n' \
          f'▫️ Всего пользователей: {count_users}\n\n' \
          f'▫️ Всего голосований: {count_polls}'

    await Sendler_msg.send_msg_message(message, msg, None)


async def no_command_start_quest(message: Message, state: FSMContext):
    """Если пользователь без состояния и команды присылает фото, то сразу стартую и создаю голосование"""

    await States.start_question.set()

    return await start_question(message, state)


async def add_btn(message: Message, state: FSMContext):
    await Sendler_msg.log_client_message(message)

    id_user = message.chat.id

    keyb = Admin_keyb().start_keyb(id_user)

    _msg = f'Что бы добавить друга нажмите кнопку ниже 👇'

    await Sendler_msg().sendler_photo_message(message, scr_friend, _msg, keyb)


def register_user(dp: Dispatcher):
    dp.register_message_handler(start, text_contains='/start', state='*')

    dp.register_message_handler(_add_friends, content_types=[types.ContentType.USER_SHARED], state='*')

    dp.register_message_handler(add_btn, text=f'/add', state='*')

    dp.register_message_handler(_add_chat, content_types=[types.ContentType.CHAT_SHARED], state='*')

    dp.register_message_handler(_my_friends, text=Admin_keyb.my_friends_btn, state='*')

    dp.register_message_handler(_my_friends, text_contains='/friends', state='*')

    dp.register_message_handler(_delete_friends, text_contains='/del_', state='*')

    dp.register_message_handler(admin, text_contains='admin', state='*')

    dp.register_message_handler(_create_poll, text=Admin_keyb.poll_btn, state='*')

    dp.register_message_handler(_create_poll, text=f'/voice', state='*')

    dp.register_message_handler(start, text_contains='')

    dp.register_poll_answer_handler(req_poll)

    dp.register_message_handler(no_command_start_quest, content_types=[types.ContentType.PHOTO])
