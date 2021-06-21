import os

regexp_for_transaction = r'[sS][eE][nN][dD]\s+([0-9]*[.,]?[0-9]+)\s+[tT][oO]\s+@(\w+)'

BOT_TOKEN = os.environ.get('BOT_TOKEN', '')
WEB_PORT = int(os.environ.get('WEB_PORT', ''))
WEB_HOST = os.environ.get('WEB_HOST', '')
WEB3_PROVIDER = os.environ.get('WEB3_PROVIDER', '')
BOT_ADMIN = os.environ.get('BOT_ADMIN', '')

if BOT_TOKEN == '':
	raise ValueError("BOT_TOKEN is not defined")

