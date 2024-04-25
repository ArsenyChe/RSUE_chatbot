from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup

button_like = InlineKeyboardButton(
    text='❤️',
    callback_data='ib_heart'
)

button_dislike = InlineKeyboardButton(
    text='💔',
    callback_data='ib_broken_heart'
)

button_thanks = InlineKeyboardButton(
    text='Спасибо за отзыв',
    callback_data='ib_button_thanks'
)

keyboard_dislike_like = InlineKeyboardMarkup(
    inline_keyboard=[[button_dislike, button_like]]
)

keyboard_thanks = InlineKeyboardMarkup(
    inline_keyboard=[[button_thanks]]
)