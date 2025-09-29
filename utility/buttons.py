from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def menu_buttons(buttons):
    keyboards = []
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for button in buttons:
        keyboards.append(KeyboardButton(text=button))

    return markup
    