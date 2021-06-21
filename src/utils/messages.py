# TODO: Remove russian comments


# START MESSAGE WHEN USER IS IN SOME CHAT
START_MESSAGE_WITH_GROUP = "Payment Bot welcomes you! To register in the bot, send ‘/register’ as a private message to the bot. Send ‘/help’ to get info for other actions."

# START MESSAGE WHEN USER IS NOT IN SOME CHAT
START_MESSAGE_WITHOUT_GROUP = "Payment Bot welcomes you! You are not recognized as a user participating in the group where deanonymization is required."

# Someone added bot to a chat
REGISTER_IN_BOT = "To have an ability to send money to participants please register in the bot %s"

# /help in chat
HELP_MESSAGE_IN_CHAT = '* To have an ability to send money to participants register in the bot %s\n'\
                       '* To transfer money to a participant send "send XX to @participantalias", where XX - value in ether\n'\
                       '* To get this message send "/help"'

# Ограничение регистрации пользователя, если он не состоит ни в одной из бесед, где зарегистрирован бот-активатор
NOT_IN_CHAT = "You are not recognized as a user participating in the group where bot is required."

# ALREADY REGISTERED
ALREADY_REGISTERED = "You have already registered."

# Пользователь попытался зарегаться но он уже зареган
REGISTER_FINISH = "Now you can send money to other people."

# Пользователь хочет удалиться но он не зареган
NOT_REGISTERED = "Not registered."

# Пользователь отправил некорректный адрес
ADDRESS_IS_INCORRECT = "Sorry, address is incorrect. Check it again."

# Пользователь попросил перевести эфир, но такого юзера нет
THERE_IS_NO_SUCH_USER = "User %s has not registered in the payment bot"

# Пользователь попросил перевести эфир, но 
USER_NOT_IN_THIS_CHAT = "User %s is not in the chat"

# Message to receiver
#                                          amount alias                              link
URL_TO_TRANSACTION_IS = "To confirm transfer %s to %s open the link in the browser:\n%s"

# Information about accout
ADDRESS_IS = "Your account: %s"

# Successful hard reset
RESET_DONE = "Database dropped"

# Reset failed
RESET_FAILED = "You are not allowed to perform such request."

# User send more than 3 txs
USER_SEND_TOO_MUCH = "You cannot requests more than 3 transfers without confirming previous requests."

#Successful changing users address
CHANGE_ADDRESS_SUCCESSFUL = "Now you will get payments to another account."

# /help in private
HELP_MESSAGE_IN_PRIVATE = "/register <account> - to register yourself\n/remove - to un-register yourself\n/change <account> - to change previosuly linked account\n/info - to get information about your account\n/list - to get the list of your transfers\n/deltx <transfer id> - to delete a transfer request from the list\n/getbalance - to get the balance\n/notification - to turn on/off notifications about unused transfers"

# /getbalance in private
BALANCE_MESSAGE_IN_PRIVATE = "Balance is %s"

# tx message
TRANSACTION_IN_LIST = "Your outstanding transfers:\n%s: %s"

# no tx in list
NO_TRANSACTIONS = "No outstanding transfers"

# fail delete request
DELETE_FAILED = "Specify your tranfser id after /deltx command"

# done delete request
DELETE_DONE = "Transaction %s was deleted"

# not admin try to get sprcial info
NON_ADMIN = "You are not allowed to perform such request."

# admin try to get sprcial info
YES_ADMIN = "Bot registered in groups:"