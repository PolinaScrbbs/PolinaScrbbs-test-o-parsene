from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, WebAppInfo,
                           InlineKeyboardMarkup, InlineKeyboardButton)

from aiogram.utils.keyboard import InlineKeyboardBuilder

start = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Парсировать')],
    [KeyboardButton(text='Получить список')],
    [KeyboardButton(text='Исходный код', web_app=WebAppInfo(url='https://github.com/PolinaScrbbs/PolinaScrbbs-test-o-parsene/tree/main'))]
],
                        resize_keyboard=True,
                        input_field_placeholder='Выберите пункт меню')

quantity_selection = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Указать количество')],
    [KeyboardButton(text='Продолжить')]
],
                        resize_keyboard=True,
                        input_field_placeholder='Выберите пункт меню')

async def inline_products(products_list):
    keyboard = InlineKeyboardBuilder()

    for j in range(len(products_list)):
        text = products_list[j]['name']
        callback_data = f"product_{products_list[j]['id']}"
        keyboard.add(InlineKeyboardButton(text=text, callback_data=callback_data))
    return keyboard.adjust(3).as_markup()


cancel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='❌', callback_data='cancel')]
])
    