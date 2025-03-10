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
global openrouter_token
global safesearch
global text_evaluator_model
global llm_type
global gemini_token

queue_to_process_everything = asyncio.Queue()

florence = None
florence_processor = None
use_florence = True
bot_display_name = "Aktiva-AI"
bot_default_avatar = "https://i.imgur.com/cWExeMh.jpeg"

bot_user = None
text_api: dict = {}
image_api: dict = {}
immersive_mode = True
blacklist_mode = True
openrouter_token =""
gemini_token=""
safesearch=None
text_evaluator_model = "deepseek-chat"

llm_type = "local"

intents: discord.Intents = discord.Intents.all()
intents.message_content = True
client: discord.Client = discord.Client(command_prefix='/', intents=intents)

