import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), 'src', '.env')

media_path = os.path.join(os.path.dirname(__file__), 'src', 'media')

load_dotenv(dotenv_path)

TOKEN = os.getenv('TOKEN')

ADMIN = ['1422194909', '7359096881']

# Сколько вариантов в голосованиях
COUNT_ANSWER_FROM_QUESTIONS = 2

START_MESSAGE = '🍀 Приветствую. Я бот - зеркало! С моей помощью ты можешь провести голосование среди своих друзей и ' \
                'например понять идут ли тебе новые очки или новый образ\n\n' \
                'Выбери вариант дальнейшей работы со мной с низу 👇 на клавиатуре'

START_QUESTION = f'💭 Для создания голосования пришлите мне следующим сообщением <b>{COUNT_ANSWER_FROM_QUESTIONS} ' \
                 f'изображения</b>, за которые нужно будет голосовать'

# Название голосования
TITLE_QUESTION = f'Я выбираю'

scr_friend = r'src/telegram/media/1.png'
