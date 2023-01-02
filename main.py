import pymongo
import dns
from aiogram import Bot, Dispatcher, executor, types
from datetime import datetime

client = pymongo.MongoClient("mongodb+srv://akhmetpekov:12345@cluster.rl2pqno.mongodb.net/?retryWrites=true&w=majority&ssl=true")

db = client['library']

TOKEN_API = "5703248993:AAHeXgVrLqORQdEUmp2jjExwZOgJAf1ehkU"

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

async def add_user(user_id, username):
    date = datetime.now().date()
    db.users.insert_one({
        "_id" : user_id,
        "username" : str("@" + username),
        "date": str(date)
    })

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text="Hello, You Are Now Registered!")
    user_id = message.chat.id
    username = message.from_user.username
    await add_user(user_id, username)

    

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)