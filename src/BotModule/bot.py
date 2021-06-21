import os
import telebot
import logging

from utils import config
from utils import mongotools
from utils import telegramtools
from utils import tools
from BotModule import Log

bot = telebot.TeleBot(config.BOT_TOKEN)

@bot.message_handler(regexp=config.regexp_for_transaction, 
                     func=lambda message : not telegramtools.in_private_message(message))
def send_transaction(message):
    """
    User sent "send 10.005 eth to @..."
    """

    Log.debug(f"User {message.from_user.username} sent {message.text}")
    text_to_send = tools.send_transaction(message)
    
    if not text_to_send is None:
        telegramtools.answer(message, text_to_send)


@bot.message_handler(func=lambda message: not message.new_chat_member is None,
                     content_types = ['new_chat_members'])    
def check_for_adding(message: telebot.types.Message):
    """
    Someone was added to a group
    """
    if message.new_chat_member.username == bot.get_me().username:
        mongotools.create_new_chat(message.chat.id)
        telegramtools.answer(message, text=tools.get_register_message())  


@bot.message_handler(func=lambda message: not message.left_chat_member is None,
                     content_types=['left_chat_member'])
def check_for_remove(message: telebot.types.Message):
    """
    Someone was removed from a group
    """
    
    if message.left_chat_member.username == bot.get_me().username:
        mongotools.delete_chat(message.chat.id)


@bot.message_handler(commands=['help'], func=lambda m : not telegramtools.in_private_message(m))
def send_help_in_group(message):
    """
    Help in some chat
    """
    
    telegramtools.answer(message, text=tools.get_register_message(in_group=True)) 


@bot.message_handler(content_types=['text'], func=telegramtools.in_private_message)
def process_text_or_command(message: telebot.types.Message):
    """
    User sent a command or text in bot's private message
    """
    Log.debug(f"User {message.from_user.username} sent {message.text}")
    text_to_send = tools.process_update(message)
    
    if text_to_send != None:
        telegramtools.answer(message, text_to_send)


    