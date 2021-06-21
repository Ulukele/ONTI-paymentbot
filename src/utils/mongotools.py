import pymongo
from utils import tools
from typing import Dict, List

def get_mongo_client():
    return pymongo.MongoClient('mongodb://root:password@mongo:27017/')

def get_mongo_db():
    return get_mongo_client().nti2019


default_user = {'chat_id': None,
                'alias': None,
                'address': None,
                'registered': False}

default_chat = {'chat_id': None}

default_transaction = {'url': None,
                        '_id': None,
                        'sender': None,
                        'amount': None,
                        'reciever': None,
                        'status': None}

def create_new_user(chat_id, alias="", address=None):
    # If user already exists
    user = users_db.find_one({'chat_id': chat_id})
    if not user is None:
        return user

    user = default_user.copy()
    user['chat_id'] = chat_id
    user['alias'] = tools.normalize_alias(alias)
    user['address'] = address

    users_db.insert_one(user)
    return user


def create_new_chat(chat_id):
    # If chat already exists
    chat = chats_db.find_one({'chat_id': chat_id})
    if not chat is None:
        return chat

    chat = default_chat.copy()
    chat['chat_id'] = chat_id
    chats_db.insert_one(chat)
    return chat

def create_new_transaction(transaction_url, transaction_id, user_address, amout_of_money, receiver_address, transaction_status):
    transaction = default_transaction.copy()
    transaction['url'] = transaction_url
    transaction['_id'] = transaction_id
    transaction['sender'] = user_address
    transaction['amount'] = amout_of_money
    transaction['receiver'] = receiver_address
    transaction['status'] = transaction_status
    transactions_db.insert_one(transaction)

def get_user(information) -> Dict:
    """
    Returns all information about user
    """

    for user_iter in users_db.find({'alias': tools.normalize_alias(information)}):
        return user_iter

    for user_iter in users_db.find({'chat_id': information}):
        return user_iter

    for user_iter in users_db.find({'address': information}):
        return user_iter

    return default_user.copy()


def get_transaction(transaction_id, user_address):
    """
    :param transaction_id: first 8 symbols of transaction id
    :param sender: wallet address of user that is trying to get information
    """
    
    for transaction in transactions_db.find({}):
        _id, sender = transaction['_id'], transaction['sender']
        if _id[:8] == transaction_id[:8] and sender == user_address:
            return transaction
    return None

def get_user_transactions(user_address):
    """
    :param sender: wallet address of user that is trying to get information
    """
    user_transactions = []
    for transaction in transactions_db.find({}):
        sender = transaction['sender']
        if sender == user_address:
            user_transactions.append(transaction)
    return user_transactions

def get_user_unpayed_transactions(user_address):
    
    user_transactions = []
    all_user_transactions = get_user_transactions(user_address)
    for transaction in all_user_transactions:
        if transaction['status'] == False:
            user_transactions.append(transaction)
    return user_transactions


def user_in_database(alias) -> bool:
    return not (get_user(alias)['chat_id'] is None)


def range_chats():
    for chat_iter in chats_db.find({}):
        yield chat_iter


def update_user(chat_id, alias=None, address=None, registered=None):
    new_user_options = {}
    for option_name, option in zip(['alias', 'address', 'registered'],
                                   [alias, address, registered]):
        if not option is None:
            new_user_options[option_name] = option

    users_db.update_one({'chat_id': chat_id}, {'$set': new_user_options})

def update_transaction_status(transaction_id, user_address, new_status):

    for transaction in transactions_db.find({}):
        _id, sender = transaction['_id'], transaction['sender']
        if _id == transaction_id:
            transaction_options = transaction.copy()
            transaction_options['status'] = new_status
            transactions_db.update_one({'_id': _id}, {'$set': transaction_options})

def delete_chat(chat_id):
    """
    delete group(chat) from the database
    """
    
    return chats_db.find_one_and_delete({'chat_id': chat_id})

def delete_transaction(transaction_id, user_address):
    transaction = get_transaction(transaction_id, user_address)
    if transaction == None:
        return None
    if transaction['status'] == True:
        return None
    return transactions_db.find_one_and_delete({'_id': transaction['_id']})


def hard_reset():
    """
    Hard reset to virgin state
    """
    
    users_db.drop()
    chats_db.drop()
    transactions_db.drop()
    

users_db = get_mongo_db().users
chats_db = get_mongo_db().chats
transactions_db = get_mongo_db().transactions

print('[INFO] >> Database has been attached\n')
