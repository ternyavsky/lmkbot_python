from concurrent.futures import thread
import logging
from platform import architecture
import fitz
import time
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from gpt import gpt
import threading
import asyncio
from utils import get_shedule, get_color
from dotenv import load_dotenv

load_dotenv(".env")

API_TOKEN = os.getenv("API_TOKEN")

# Configure logging
logging.basicConfig(level=logging.INFO)


bot = Bot(API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=bot)



kb = [
    [types.KeyboardButton(text='Замены'), 
         types.KeyboardButton(text="Цвет недели")]
    ]


keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

@dp.message_handler(commands=['start'], )
async def send_welcome(message: types.Message):
    start = time.time()
    await message.reply(f"Привет, {message.chat.first_name}! Это бот иcип, замены и цвет недели - здесь", reply_markup=keyboard)
    print(time.time() - start)

@dp.message_handler(commands=["help"])
async def send_help(message):
    await message.reply(f"<b>/help</b> - Информация о командах\n<b>/ask</b> - Chat GPT. Пример использования: /ask Кто такой Артуро Сандоваль ?", reply_markup=keyboard)


@dp.message_handler(content_types=['text'])
async def color_week(message):
    start = time.time()
    if message.text == 'Цвет недели':
        a = get_color()
        await message.answer(a)

    if message.text == 'Замены':
        start = time.time()
        print('work')
        a = get_shedule()
        doc = fitz.open("shedule.pdf")
        media = types.MediaGroup()
        for i in range(len(doc)):
            page = doc.load_page(i)  # number of page
            pix = page.get_pixmap()
            output = "page"+str(i+1)+".png" # first create the output folder in the destination
            pix.save(output)
            if len(doc) - 1 == i:
                media.attach_photo(photo=types.InputFile(output), caption=a)
            else:
                media.attach_photo(photo=types.InputFile(output))
        end = print(time.time() - start)
        await message.answer_media_group(media=media)

    if "/ask" in message.text:
        text = " ".join(message.text.split()[1:])
        await message.answer(f"@{message.chat.username}, ожидайте...", reply_markup=keyboard)
        asyncio.create_task(gpt(message, text))
        
    
        

        

        
if __name__ == '__main__':
    executor.start_polling(dp)
