import telegram.ext
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode
import time
import mines
from minerator import *
import numpy as np
from PIL import Image
from matplotlib import cm
from io import BytesIO
import cv2

import logging

users_list = []
chat_ids = []
imager = Minerator()
print('Clearing variable')
game = {}
bio = BytesIO()

def start(update, context):
    #print(update['message']['chat']['username'])
    name = update['message']['chat']['username']
    if name not in users_list:
        users_list.append('@'+str(name))
    if update.message.chat_id not in chat_ids:
        chat_ids.append(update.message.chat_id)
    context.bot.send_message(chat_id=update.message.chat_id, text="Hi dude, let's play a minesweeper!")
    custom_keyboard = [['Easy 8x8'], ['Medium 11X11'], ['Hard 15x15']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    context.bot.send_message(chat_id=update.message.chat_id, text="Choose the difficulty!", reply_markup=reply_markup)

def field(update, context, x, y, n):
    game[str(update.message.chat_id)] = mines.Minesweeper(x,y,n)
    print(game[str(update.message.chat_id)])
    game[str(update.message.chat_id)].print_field()
    # cv2.imshow('Dimas', imager.get_image(game[str(update.message.chat_id)].mask))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    cv2.imwrite(str(update.message.chat_id) + '.png',imager.get_image(game[str(update.message.chat_id)].mask))
    #im = Image.fromarray(imager.get_image(game[str(update.message.chat_id)].mask))
    # bio.name = 'image.jpeg'
    # im.save(bio, 'JPEG')
    # bio.seek(0)
    context.bot.send_photo(update.message.chat_id, open(str(update.message.chat_id) + '.png', 'rb'))

    # msg = ''.join(''.join(str(mine) + ' ' for mine in line) + '\n' for line in game[str(update.message.chat_id)].mask)
    # context.bot.send_message(chat_id=update.message.chat_id, text = msg)
    context.bot.send_message(chat_id=update.message.chat_id, text = "Pick up # writing coordinates, like:" + "\n" + "5 6")

def coo(update, context):
    if str(update.message.chat_id) not in game or game[str(update.message.chat_id)] is None:
        context.bot.send_message(chat_id=update.message.chat_id, text = 'You don`t have pending games')
        custom_keyboard = [['Easy 8x8'], ['Medium 11X11'], ['Hard 15x15']]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        context.bot.send_message(chat_id=update.message.chat_id, text= 'Start one!', reply_markup = reply_markup)
        return
    if game[str(update.message.chat_id)].state != 0:
        context.bot.send_message(chat_id=update.message.chat_id, text = 'Previous game is finished, start a new one')
        return
    x, y = update.message.text.split(' ')
    x = int(x)
    y = int(y)
   
    game[str(update.message.chat_id)].open_field(x-1,y-1)

    # cv2.imshow('Dimas', imager.get_image(game[str(update.message.chat_id)].mask))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    cv2.imwrite(str(update.message.chat_id) + '.png',imager.get_image(game[str(update.message.chat_id)].mask))
    context.bot.send_photo(update.message.chat_id, open(str(update.message.chat_id) + '.png', 'rb'))
    # msg = ''.join(''.join(str(mine) + ' ' for mine in line) + '\n' for line in game[str(update.message.chat_id)].mask)
    # context.bot.send_message(chat_id=update.message.chat_id, text = msg)
    state = game[str(update.message.chat_id)].check_victory()
    custom_keyboard = [['Easy 8x8'], ['Medium 11X11'], ['Hard 15x15']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    if state == 1:
        context.bot.send_message(chat_id=update.message.chat_id, text = 'Hah, U lost!')
        context.bot.send_message(chat_id=update.message.chat_id, text= 'Try ones more!', reply_markup = reply_markup)
    if state == 2:
        context.bot.send_message(chat_id=update.message.chat_id, text = 'Hah, u won')
        context.bot.send_message(chat_id=update.message.chat_id, text="Try ones more!", reply_markup = reply_markup)

def users(update, context):
        context.bot.send_message(chat_id=update.message.chat_id, text=str(users_list))

def keyboard(update, context):
    if update.message.text == 'Easy 8x8':
        field(update, context, 8, 8, 10)
    elif update.message.text == 'Medium 11X11':
        field(update, context, 11, 11, 12)
    elif update.message.text == 'Hard 15x15':
        field(update, context, 15,15, 18)
    else:
        coo(update, context)

def main():
    updater = Updater(token='TOKEN', use_context=True)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(CommandHandler('users', users))
    dispatcher.add_handler(CommandHandler('field', field))
    key_handler = MessageHandler(Filters.text, keyboard)
    dispatcher.add_handler(key_handler)
    updater.start_polling()

if __name__=='__main__':
    main()