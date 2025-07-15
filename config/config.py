import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

moderation_role_id = [1, 2]