import asyncio
from aiogram import types
import openai
import os 
from dotenv import load_dotenv
import aiohttp
import wandb
import requests

load_dotenv(".env")

api_key = os.getenv("OPENAI_API_TOKEN")


kb = [
    [types.KeyboardButton(text='Замены'), 
         types.KeyboardButton(text="Цвет недели")]
    ]

keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

models = openai.Model.list()

# print the first model's id
print(models.data[0].id)


async def gpt(message, text):
# create a chat completion
   chat_completion = await openai.ChatCompletion.acreate(model="gpt-3.5-turbo", messages=[{"role": "user", "content": text}])

# print the chat completion
   await message.answer(f"@{message.chat.username}, {chat_completion.choices[0].message.content}", reply_markup=keyboard)

