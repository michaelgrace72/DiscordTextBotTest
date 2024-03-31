import dotenv
import os
import requests
import discord
import responses
from typing import Final

dotenv.load_dotenv()

TOKEN: Final[str] = os.getenv('TOKEN')
