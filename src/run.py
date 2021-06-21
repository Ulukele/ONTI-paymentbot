import threading

from BotModule.bot import bot
from ServerModule.Server import Server
from utils.tools import get_function_with_bot_instance
from utils.config import WEB_PORT


if __name__ == "__main__":
    print(f'==========================\nHello from @{bot.get_me().username}!\n==========================\n')

    print('[INFO] >> Removing webhook\n')
    bot.delete_webhook()

    print('[INFO] >> Creating server')
    s = Server(WEB_PORT, get_function_with_bot_instance(bot))

    print('[INFO] >> Starting thread with server')
    t = threading.Thread(target=s.run)
    t.start()

    print('[INFO] >> Starting polling ...\n')
    bot.polling()

