import os
import discord
from dotenv import load_dotenv
import asyncio


load_dotenv()
global text_api
global image_api
global character_card

global immersive_mode
global blacklist_mode

queue_to_process_everything = asyncio.Queue()

florence = None
florence_processor = None

bot_display_name = "Aktiva-AI"
bot_default_avatar = "https://i.imgur.com/mxlcovm.png"

text_api: dict = {}
image_api: dict = {}
immersive_mode = True
blacklist_mode = False

intents: discord.Intents = discord.Intents.all()
intents.message_content = True
client: discord.Client = discord.Client(command_prefix='/', intents=intents)

