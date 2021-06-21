from telebot import TeleBot
from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
import telebot
import logging

from BotModule import bot as BotModule
from BotModule import Log
from utils import messages


def answer(message: Message, text: str, parse_mode=None, reply_markup=None):
    send_message(message.chat.id, text, parse_mode=parse_mode, reply_markup=reply_markup)


def send_message(chat_id, text, parse_mode=None, reply_markup=None):
    try:
        sended_message = BotModule.bot.send_message(chat_id, text, 
                                          parse_mode=parse_mode, 
                                          reply_markup=reply_markup)
        return sended_message
    except telebot.apihelper.ApiException as e:
        if 'bot was kicked' in e.args[0]:
            logging.exception(Exception(f"Bot has kicked from group {message.chat.id}."))
        else:
            logging.exception(e)
        

def get_alias():
    return '@' + BotModule.bot.get_me().username

def user_in_chat(chat_id, user_id):
    
    
    try:
        Log.debug(BotModule.bot.get_chat_member(chat_id, user_id).status)
        result = BotModule.bot.get_chat_member(chat_id, user_id).status != 'left'
        Log.debug(f"User [{user_id}] in chat [{chat_id}]: {result}")
        return result
    except telebot.apihelper.ApiException as e:
        if 'user not found' in e.args[0]:
            Log.debug(f"User [{user_id}] in chat [{chat_id}]: {False}")
            return False
        else:
            logging.exception(e)


def in_private_message(message) -> bool:
    return message.chat.type == "private"


def bot_was_mentioned(message) -> bool:
    if message.text is None:
        return False
    return get_alias() in message.text