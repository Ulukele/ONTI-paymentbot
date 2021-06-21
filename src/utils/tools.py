import re
from typing import List
from telebot import TeleBot
from datetime import datetime
import logging

from utils import mongotools
from utils.User import User
from utils import telegramtools
from utils.blockchaintools import toWei, fromWei, CHAIN_ID
from utils import messages
from utils.config import regexp_for_transaction, WEB_HOST, WEB_PORT


def process_update(message) -> str:
    """
    Return a message to send to the user 
    in response to a command or text
    """

    # Message was sent to a PM, so create new user
    if not mongotools.user_in_database(message.from_user.username):
        db_user = mongotools.create_new_user(message.from_user.id, 
                                             normalize_alias(message.from_user.username))
    else:
        db_user = mongotools.get_user(message.from_user.id)

    # Create USER instance
    user = User(alias=db_user['alias'], registered=db_user['registered'], 
                address=db_user['address'], in_some_group=user_in_some_chat(message.from_user.id))

    # Do transitions
    text_to_send = user.action(message)
    
    # Update database
    user.update(message.from_user.id)

    return text_to_send


def send_transaction(message):
    # TODO: description of the method

    user_from = mongotools.get_user(message.from_user.username) 
    
    # If user_from NOT in database
    if not user_from['registered']:
        return messages.REGISTER_IN_BOT % telegramtools.get_alias()

    amount, alias = parse_text(message.text)
    user_to = mongotools.get_user(alias)
    
    # If user_to NOT in database
    if not user_to['registered']:
        return messages.THERE_IS_NO_SUCH_USER % alias
    
    # If user_to is NOT in this chat
    if not telegramtools.user_in_chat(message.chat.id, user_to['chat_id']):
        return messages.USER_NOT_IN_THIS_CHAT % alias
    
    # If user_to in this chat and 
    # all users are registered in the bot

    address_from, address_to = user_from['address'], user_to['address']

    
    if len(mongotools.get_user_unpayed_transactions(address_from)) >= 3:
        telegramtools.send_message(message.from_user.id, messages.USER_SEND_TOO_MUCH)
        return

    # Unique and non-predictable ID
    transaction_id = str(abs(hash(address_from + address_to + str(amount) + str(datetime.timestamp(datetime.now())))))

    # Generate url
    url = generate_url(transaction_id, address_to, toWei(amount, 'ether'))

    mongotools.create_new_transaction(transaction_url=url, transaction_id=transaction_id, user_address=address_from, amout_of_money=amount, receiver_address=address_to, transaction_status=False)

    # Send to PM url
    telegramtools.send_message(message.from_user.id, messages.URL_TO_TRANSACTION_IS % (amount, alias, url))


def generate_url(transaction_id, address, amount):
    URL = f'http://{WEB_HOST}:{WEB_PORT}/?id={transaction_id}&link="ethereum:{address}@{CHAIN_ID}?value={amount}"'
    return URL

def get_function_with_bot_instance(bot_instance: TeleBot):
    def accept_result_from_server(res):
        # Write it by yourself ;)
        pass
    return accept_result_from_server    
    
def parse_text(text):
    """
    Parse text and return amount and alias
    """
    
    match = re.match(regexp_for_transaction, text)
    return match.group(1), normalize_alias(match.group(2))


def user_in_some_chat(user_id) -> bool:
    """
    Check all chats and return true if user is in some chat
    """

    for chat in mongotools.range_chats():
        if telegramtools.user_in_chat(chat['chat_id'], user_id):
            return True
    return False


def normalize_alias(alias) -> str:
    """
    Returns alias with '@'
    """
    return '@' + str(alias).replace('@', '')


def get_register_message(in_group=False):
    if in_group:
        return messages.HELP_MESSAGE_IN_CHAT % telegramtools.get_alias()
    
    return  messages.REGISTER_IN_BOT % telegramtools.get_alias()