import os
from dotenv import load_dotenv

load_dotenv()

TOKEN_API = os.getenv("API_TOKEN")
PROVIDER_TOKEN = os.getenv("provider_token")

MAIN_CHANNEL_ID = int(os.getenv("mainch"))
ANNOUNCE_CHANNEL_ID = int(os.getenv("annch"))

BOT_LINK = os.getenv("botlink")
CHANNEL_LINK = os.getenv("clink")

ADMIN_ID = int(os.getenv("admid"))