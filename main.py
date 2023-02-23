import pymongo
import dns
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils import executor
from aiogram.types import ParseMode
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from gridfs import GridFS
from io import BytesIO
from datetime import datetime
from keyboards import mainMenuKB


client = pymongo.MongoClient("mongodb+srv://akhmetpekov:1234@cluster0.3qu2inj.mongodb.net/?retryWrites=true&w=majority")

db = client['library']

TOKEN_API = "5703248993:AAHeXgVrLqORQdEUmp2jjExwZOgJAf1ehkU"

fs = GridFS(db, collection="book_files")

bot = Bot(TOKEN_API)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=MemoryStorage())



async def add_user(user_id, username):
    date = datetime.now().date()
    db.users.insert_one({
        "_id" : user_id,
        "username" : str("@" + username),
        "date": str(date)
    })

class UploadBookStates(StatesGroup):
    TITLE = State()
    AUTHOR = State()
    TAGS = State()
    UPLOAD = State()

class SearchBook(StatesGroup):
    waiting_for_title = State()

@dp.message_handler(Text(equals="Upload"))
async def upload_book(message: types.Message):
    await message.answer("Please enter the book title:")
    await UploadBookStates.TITLE.set()

@dp.message_handler(state=UploadBookStates.TITLE)
async def get_book_title(message: types.Message, state: FSMContext):
    # Save book title in FSM
    await state.update_data(title=message.text)

    # Move to next state (author)
    await message.answer("Please enter the book author:")
    await UploadBookStates.AUTHOR.set()

@dp.message_handler(state=UploadBookStates.AUTHOR)
async def get_book_author(message: types.Message, state: FSMContext):
    # Save book author in FSM
    await state.update_data(author=message.text)

    # Move to next state (tags)
    await message.answer("Please enter the book tags separated by commas:")
    await UploadBookStates.TAGS.set()

@dp.message_handler(state=UploadBookStates.TAGS)
async def get_book_tags(message: types.Message, state: FSMContext):
    # Save book tags in FSM
    tags = message.text.split(",")
    await state.update_data(tags=tags)

    # Move to next state (upload)
    await message.answer("Please upload your pdf file at this link(https://pdfhost.io/) and paste the link:")
    await UploadBookStates.UPLOAD.set()

@dp.message_handler(state=UploadBookStates.UPLOAD)
async def upload_book(message: types.Message, state: FSMContext):
    # Save book to MongoDB Atlas
    await state.update_data(upload=message.text)
    user_id = message.chat.id
    username = message.from_user.username
    date = datetime.now().date().strftime('%Y-%m-%d')
    data = await state.get_data()
    book_data = {
        "user_id": user_id,
        "title": data["title"],
        "author": data["author"],
        "tags": data["tags"],
        "pdf_link": data['upload'],
        "username": username,
        "date":date
    }
    db.books.insert_one(book_data)

    # End the conversation and send confirmation message
    await message.answer("Book uploaded successfully!", reply_markup=mainMenuKB)
    await state.finish()






@dp.message_handler(Text(equals="Search"))
async def search_command(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    await bot.send_message(chat_id=message.chat.id, text='Enter the title of the book:')
    await SearchBook.waiting_for_title.set()

@dp.message_handler(Text(equals="Upload"))
async def upload_handler(message: types.Message):
    await upload_book(message)

@dp.callback_query_handler(lambda c: True)
async def process_callback(callback_query: types.CallbackQuery):
    callback_data = callback_query.data
    book_title, book_link = callback_data.split("|")
    message = f"Link to pdf of {book_title}: {book_link}"
    await bot.send_message(chat_id=callback_query.message.chat.id, text=message)
    await bot.answer_callback_query(callback_query.id)

@dp.message_handler(state=SearchBook.waiting_for_title)
async def process_title(message: types.Message, state: FSMContext):
    # Get the title of the book from the user's message
    async with state.proxy() as data:
        data['name'] = message.text

        book_title = data["name"]
        pattern = f".*{book_title}.*"

        books = db.books.find({"title": {"$regex": pattern, "$options": "i"}})
        counter = 0
        keyboard = types.InlineKeyboardMarkup()
        for book in books:
            counter += 1
            callback_data = f"{book['title']}|{book['pdf_link']}"
            keyboard.add(types.InlineKeyboardButton(text=book['title'], callback_data=callback_data))
        if counter >= 1:
            await bot.send_message(chat_id=message.chat.id, text="Please select a book:", reply_markup=keyboard)
        else:
            await bot.send_message(chat_id=message.chat.id, text="No books found with the given title!")
            



        # Reset the state
        await state.finish()


@dp.message_handler(Text(equals="Catalog"))
async def catalog_command_handler(message: types.Message):
    # Get all books from the collection
    books = db.books.find()
    counter = 0
    keyboard = types.InlineKeyboardMarkup()
    for book in books:
        counter += 1
        button_text = f"{book['title']} - {book['author']}"
        callback_data = f"{book['title']}|{book['pdf_link']}"
        keyboard.add(types.InlineKeyboardButton(text=button_text, callback_data=callback_data))
    if counter >= 1:
        await bot.send_message(chat_id=message.chat.id, text="Please select a book:", reply_markup=keyboard)
    else:
        await bot.send_message(chat_id=message.chat.id, text="No books found")


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.send_message(chat_id=message.chat.id, text="Hello, You Are Now Registered!", reply_markup=mainMenuKB)
    user_id = message.chat.id
    username = message.from_user.username
    await add_user(user_id, username)

    

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)