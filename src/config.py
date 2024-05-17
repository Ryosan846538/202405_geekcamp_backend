from dotenv import load_dotenv
load_dotenv()

import os

YOUR_CHANNEL_SECRET = os.getenv('YOUR_CHANNEL_SECRET')
YOUR_CHANNEL_ACCESS_TOKEN = os.getenv('YOUR_CHANNEL_ACCESS_TOKEN')
SPECIAL_ID = os.getenv('SPECIAL_ID')