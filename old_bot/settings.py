import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), "src", ".env")

media_path = os.path.join(os.path.dirname(__file__), "src", "media")

load_dotenv(dotenv_path)

TOKEN = "7680771181:AAETBZfAoRHy8zfoaDybzozcyuz1N4ovYNE"

ADMIN = ["1422194909", "7359096881"]

# Сколько вариантов в голосованиях
COUNT_ANSWER_FROM_QUESTIONS = 2

START_MESSAGE = "🍀 Improve image bot"

START_QUESTION = (
    f"💭 to improve image type improve image and send one picture to the bot to improve"
)

# Название голосования
TITLE_QUESTION = f"Я выбираю"

scr_friend = r"src/telegram/media/1.png"
