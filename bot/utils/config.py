import os

from dotenv import load_dotenv

# Environment variables
load_dotenv()

token = os.getenv("BOT_TOKEN")
server_url = os.getenv("SERVER_URL")
exhibition_url = os.getenv("EXHIBITION_URL")
event_program_url = os.getenv("EVENT_PROGRAM_URL")
