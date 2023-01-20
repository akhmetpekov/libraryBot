import pymongo
import dns
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from datetime import datetime
from keyboards import mainMenuKB, profileKB

kanat = "Kanat"

client = pymongo.MongoClient("mongodb+srv://akhmetpekov:qwerty123a  `@cluster0.3qu2inj.mongodb.net/?retryWrites=true&w=majority")

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

async def upload_book(user_id, username, title,author,available,keywords):
    date = datetime.now().date()
    db.books.insert_one({
        "_id" : user_id,
        "title":title,
        "author":author,
        "available":available,
        "keywords":keywords,
        "username" : str("@" + username),
        "date": date
    })



@dp.message_handler(Text(equals="Profile"))
async def profile_menu(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    await bot.send_message(message.chat.id, "Your Proifile", reply_markup=profileKB)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.send_message(chat_id=message.chat.id, text="Hello, You Are Now Registered!", reply_markup=mainMenuKB)
    user_id = message.chat.id
    username = message.from_user.username
    await add_user(user_id, username)

    

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)