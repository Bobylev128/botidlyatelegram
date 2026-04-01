import os
from dotenv import load_dotenv

load_dotenv()

TOKEN_API = os.getenv("API_TOKEN")
PROVIDER_TOKEN = os.getenv("provider_token")

MAIN_CHANNEL_ID = int(os.getenv("mchid"))
ANNOUNCE_CHANNEL_ID = int(os.getenv("achid"))

BOT_LINK = os.getenv("botlink")
CHANNEL_LINK = os.getenv("chlink")

ADMIN_ID = int(os.getenv("admid"))
