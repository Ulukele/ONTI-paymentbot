import os
import logging

Log = logging.getLogger('bot_solution')

# Default level is INFO.
#Log.setLevel(logging.DEBUG if os.environ.get('DEBUG') == 'True' else logging.INFO)
Log.setLevel(logging.DEBUG)

# Log to file.
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

Log.addHandler(handler) 
