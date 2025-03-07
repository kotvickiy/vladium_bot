import io
import asyncio
import speech_recognition as sr

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from pydub import AudioSegment

from config import TG_TOKEN


bot = Bot(token=TG_TOKEN)
dp = Dispatcher()
recognizer = sr.Recognizer()


@dp.message(F.voice)
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
    except Exception:
        text = 'Что-то пошло не так. Попробуй еще раз.'
    await message.answer(text)


@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    await message.answer("Отправь мне голосовое сообщение, и я попробую его расшифровать.")


@dp.message(F.voice)
async def voice_message_handler(message: types.Message):
    voice = message.voice
    await voice_message(voice)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
