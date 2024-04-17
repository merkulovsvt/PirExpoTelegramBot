import os

from dotenv import load_dotenv

# Environment variables
load_dotenv()

token = os.getenv("BOT_TOKEN")
