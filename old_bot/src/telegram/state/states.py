import asyncio

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from settings import COUNT_ANSWER_FROM_QUESTIONS
from src.business.logic.delete_user_file import delete_file
from src.business.logic.split_media_sql import split_media_sql
from src.business.logic.write_chat import new_writer_chat
from src.business.poll_create.add_user_files.add_user_files import add_user_files
from src.business.poll_create.send_media_poll.send_media_poll import send_media_poll
from src.telegram.sendler.sendler import Sendler_msg

from src.telegram.bot_core import BotDB


class States(StatesGroup):
    media_group_saver = {}

    start_question = State()


async def start_question(message: Message, state: FSMContext):
    id_user = message.chat.id

    await new_writer_chat(id_user)

    await Sendler_msg.log_client_message(message)

    type_msg = message.content_type

    if type_msg != 'photo':
        msg = f'⚠️ Вы прислали не фотографии. Пожалуйста пришлите следующим сообщением фотографии для создания ' \
              f'голосования!'

        await Sendler_msg.send_msg_message(message, msg, None)

        return False

    if not message.media_group_id:
        msg = f'⚠️ Вы прислали одно изображение. Необходимо прислать {COUNT_ANSWER_FROM_QUESTIONS} изображений. ' \
              f'Пожалуйста пришлите следующим сообщением изображения для создания голосования!'

        await Sendler_msg.send_msg_message(message, msg, None)

        return False

    media_group_name = f'media_group-{message.media_group_id}'

    media_group_exist = States.media_group_saver.get(media_group_name, False)

    name_stream = message.message_id

    if not media_group_exist:
        States.media_group_saver[media_group_name] = True
        States.media_group_saver[id_user] = {'streams': []}
    else:
        States.media_group_saver[id_user]['streams'].append(name_stream)

    id_pk = await add_user_files(message)

    if media_group_exist:
        States.media_group_saver[id_user]['streams'].remove(name_stream)

        try:
            await message.bot.delete_message(id_user, message.message_id)
        except:
            pass

        return True

    # На всякий ждём что бы новые потоки точно успели прийти
    await asyncio.sleep(1)

    # Жду когда все потоки обработают себя
    count_wait = 0

    # Жду когда все потоки завершат обработку, или максимум 2 минуты
    while States.media_group_saver[id_user]['streams']:
        await asyncio.sleep(1)

        if count_wait < 120:
            break

        count_wait += 1

        continue

    try:
        await message.bot.delete_message(id_user, message.message_id)
    except:
        pass

    media_poll = BotDB.get_media_poll(id_pk)

    files_path = await split_media_sql(media_poll[4])

    count_media = (len(files_path))

    if count_media > COUNT_ANSWER_FROM_QUESTIONS:
        error_msg = f'⚠️ Максимум {COUNT_ANSWER_FROM_QUESTIONS} изображения.\n\n' \
                    f'В голосования вы можете добавлять максимум {COUNT_ANSWER_FROM_QUESTIONS} изображения. ' \
                    f'Выберите нужные варианты и попробуйте ещё раз прислать мне {COUNT_ANSWER_FROM_QUESTIONS} ' \
                    f'изображения, которые нужно оценить'

        await Sendler_msg.send_msg_message(message, error_msg, None)

        await delete_file(files_path)

        return False

    await state.finish()

    await new_writer_chat(id_user)

    res_send_media_poll = await send_media_poll(id_user, media_poll)

    del States.media_group_saver[media_group_name]

    await delete_file(files_path)

    return True


def register_state(dp: Dispatcher):
    dp.register_message_handler(start_question, state=States.start_question, content_types=[types.ContentType.ANY])
