import io
import speech_recognition as sr

from aiogram import Bot, F, Router, types
from aiogram.filters import CommandStart
from pydub import AudioSegment

import app.keyboards as kb

from config import TG_TOKEN
from app.function import text_processor
from app.ai import ai


bot = Bot(token=TG_TOKEN)
router = Router()
recognizer = sr.Recognizer()


@router.message(F.voice)
async def voice_message(message: types.Message):
    try:
        voice_file = await bot.get_file(message.voice.file_id)
        file_path = voice_file.file_path
        file_bytes = await bot.download_file(file_path)
        ogg_stream = io.BytesIO(file_bytes.getvalue())
        audio = AudioSegment.from_ogg(ogg_stream)
        wav_stream = io.BytesIO()
        audio.export(wav_stream, format="wav")
        wav_stream.seek(0)
        with sr.AudioFile(wav_stream) as source:
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language="ru-RU")
    except Exception as ex:
        print(ex)
        text = 'Что-то пошло не так. Попробуй еще раз.'
    await message.answer(ai(text))


@router.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    await message.answer("Отправь мне голосовое сообщение или выбери меню.", reply_markup=kb.main)


@router.message(F.text == 'Меню')
async def menu_handler(message: types.Message):
    await message.answer("Меню", reply_markup=kb.settings)
