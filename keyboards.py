from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

mainMenuKB = ReplyKeyboardMarkup(resize_keyboard=True)
mmkb1 = KeyboardButton('Profile')
mmkb2 = KeyboardButton('Search')
mmkb3 = KeyboardButton('Catalog')
mmkb4 = KeyboardButton('Upload')
mainMenuKB.add(mmkb2).insert(mmkb3).add(mmkb4)


catalogKB = InlineKeyboardMarkup(row_width=2)
ckb1 = InlineKeyboardButton("", url="")
ckb2 = InlineKeyboardButton("", url="")
ckb3 = InlineKeyboardButton("", url="")
ckb4 = InlineKeyboardButton("", url="")
ckb5 = InlineKeyboardButton("", url="")
ckb6 = InlineKeyboardButton("", url="")
catalogKB.add(ckb1, ckb2, ckb3, ckb4, ckb5, ckb6)