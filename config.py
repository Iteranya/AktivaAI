import os
import discord
from dotenv import load_dotenv
import asyncio


load_dotenv()
global text_api
global image_api
global character_card
global tts_config, tts_model, gpt_cond_latent, speaker_embedding

queue_to_process_everything = asyncio.Queue()

florence = None
florence_processor = None

tts_config = None
tts_model = None
gpt_cond_latent = None
speaker_embedding = None
bot_display_name = "Aktiva-AI"
bot_default_avatar = "https://i.imgur.com/mxlcovm.png"

text_api: dict = {}
image_api: dict = {}

# Dictionary to keep track of the bot's last message time and last mentioned channel by guild
bot_last_message_time = {}
bot_last_mentioned_channel = {}
intents: discord.Intents = discord.Intents.all()
intents.message_content = True
client: discord.Client = discord.Client(command_prefix='/', intents=intents)

