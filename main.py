import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()

client = MongoClient(getenv("MONGODB_URI"))
db = client["cluster-pro"]

collection = db["users"]

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user = collection.find_one({"user_id": message.from_user.id})
    if user:
        await message.answer("Hello, welcome back!")
    else:
        payload = {
            "user_id": message.from_user.id,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "username": message.from_user.username,
            "createdAt": message.date,
            "accepted_tos": False
        }
        collection.insert_one(payload)
        await message.answer("Hello, new user!")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())