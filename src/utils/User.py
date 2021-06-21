from telebot.types import Message
from web3 import Web3

from utils import mongotools
from utils import messages
from utils import tools
from utils import blockchaintools
from utils.config import  BOT_ADMIN

class User:
    """
    User instance

    Before processing a user request (command or text), 
    a User instance with all parameters is created 
    It processed, and changes are loaded to the database.
    """

    def __init__(self, alias, registered, address, in_some_group):
        self.alias = alias
        self.registered = registered
        self.address = address
        self.in_some_group = in_some_group

    def action(self, message: Message):
        text = message.text

        # If text is not a command
        if text.startswith('/start'):
            return self.__start(message)

        elif text.startswith('/register'):
            return self.__register(message)

        elif text.startswith('/reset'):
            return self.__reset(message)

        # Following commands require user to be registered
        # so check if user is registered
        elif not self.registered:
            return messages.NOT_REGISTERED

        elif text.startswith('/remove'):
            return self.__remove(message) 

        elif text.startswith('/info'):
            return self.__info(message)

        elif text.startswith('/change'):
            return self.__change(message)

        elif text.startswith('/help'):
            return self.__help(message)

        elif text.startswith('/getbalance'):
            return self.__getbalance(message)

        elif text.startswith('/listgroups'):
            return self.__listgroups(message)
        
        elif text.startswith('/list'):
            return self.__list(message)

        elif text.startswith('/deltx'):
            return self.__deltx(message)

        
    def __start(self, message):
        if self.in_some_group:
            return messages.START_MESSAGE_WITH_GROUP
        return messages.START_MESSAGE_WITHOUT_GROUP


    def __register(self, message):
        if not self.in_some_group:
            return messages.NOT_IN_CHAT

        if self.registered:
            return messages.ALREADY_REGISTERED

        try:
            # oops
            assert len(message.text.split()) == 2
            address = blockchaintools.check_pub_key(message.text.split()[1]) 
        except (ValueError, IndexError, AssertionError):
            return messages.ADDRESS_IS_INCORRECT

        self.address = address
        self.registered = True
        return messages.REGISTER_FINISH
    

    def __remove(self, message):
        # remove all transactions where the sender is user
        mongotools.transactions_db.delete_many({'sender': self.address}).deleted_count
        
        # unregister user
        self.registered = False
        return messages.START_MESSAGE_WITH_GROUP


    def __info(self, message):
        return messages.ADDRESS_IS % self.address


    def __reset(self, message):
        if message.from_user.username == BOT_ADMIN:
            mongotools.hard_reset()
            return messages.RESET_DONE
        return messages.RESET_FAILED

    def update(self, chat_id):
        mongotools.update_user(chat_id, alias=self.alias, 
                               address=self.address, registered=self.registered)

    def __change(self, message):
        try: # проверка корректности адреса
            # oops
            assert len(message.text.split()) == 2
            address = blockchaintools.check_pub_key(message.text.split()[1])
        except (ValueError, IndexError, AssertionError):
            return messages.ADDRESS_IS_INCORRECT

        # TODO проверка на неподтвержденный платеж

        self.address = address

        return messages.CHANGE_ADDRESS_SUCCESSFUL
    
    def __help(self, message):
        return messages.HELP_MESSAGE_IN_PRIVATE

    def __getbalance(self, message):
        balance = str(blockchaintools.getBalance(address=self.address)/pow(10,18))
        return messages.BALANCE_MESSAGE_IN_PRIVATE % balance

    def __list(self, message):
        tx_list = mongotools.get_user_unpayed_transactions(user_address=self.address)
        if len(tx_list) == 0:
            return messages.NO_TRANSACTIONS
        big_msg = []
        for tx in tx_list:
            msg = messages.TRANSACTION_IN_LIST % (tx['_id'][:8], tx['url'])
            big_msg.append(msg)
        return '\n'.join(big_msg)

    def __deltx(self, message):
        
        assert len(message.text.split()) == 2
        id_ = message.text.split()[1]
        res = mongotools.delete_transaction(transaction_id=id_, user_address=self.address)
        if res == None:
            return messages.DELETE_FAILED
        else:
            return messages.DELETE_DONE % id_
    
    def __listgroups(self, message):

        if self.alias != BOT_ADMIN:
            return messages.NON_ADMIN
        msg = messages.YES_ADMIN
        for some_chat in mongotools.range_chats():
            msg = msg + '\n' + some_chat['chat_id']
        if msg == messages.YES_ADMIN:
            return "None"
        else:
            return msg