from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

mainMenuKB = ReplyKeyboardMarkup(resize_keyboard=True)
mmkb1 = KeyboardButton('Profile')
mmkb2 = KeyboardButton('Search')
mmkb3 = KeyboardButton('Catalog')
mainMenuKB.add(mmkb1).add(mmkb2).insert(mmkb3)

profileKB = InlineKeyboardMarkup(row_width= 3)
pkb1 = InlineKeyboardButton('Favourites', url='google.com')
pkb2 = InlineKeyboardButton('Profile Photo', url='google.com')
pkb3 = InlineKeyboardButton('Statistics', url='google.com')
profileKB.add(pkb1, pkb2).add(pkb3)

