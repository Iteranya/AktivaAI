import asyncio
import os
import discord
from discord import app_commands
from discord import Intents
from discord import Client
import logging
import argparse
import config

import util

from discord import app_commands
from dotenv import load_dotenv
import src.observer as observer

import main
from unittest.mock import patch
from transformers.dynamic_module_utils import get_imports
from transformers import AutoProcessor, AutoModelForCausalLM 
import warnings
from huggingface_hub import file_download
import src.controller as controller
import src.function as fun

# Suppress the specific FutureWarning from huggingface_hub
warnings.filterwarnings("ignore", category=FutureWarning, module="huggingface_hub.file_download")
warnings.filterwarnings("ignore", category=UserWarning, module="torch.utils")


load_dotenv()
discord_token: str | None = os.getenv("DISCORD_TOKEN")
openrouter_token: str | None = os.getenv("OPENROUTER_TOKEN")
if discord_token is None:
    raise RuntimeError("$DISCORD_TOKEN env variable is not set!")
if openrouter_token is None:
    openrouter_token=""
client = config.client
config.openrouter_token = openrouter_token

def fixed_get_imports(filename: str | os.PathLike) -> list[str]:
    # if not str(filename).endswith("modeling_florence2.py"):
    #     return get_imports(filename)
    imports = get_imports(filename)
    if "flash_attn" in imports:
        imports.remove("flash_attn")
    return imports

with patch("transformers.dynamic_module_utils.get_imports"):
    config.florence = AutoModelForCausalLM.from_pretrained("MiaoshouAI/Florence-2-base-PromptGen-v2.0", 
                                                        trust_remote_code=True)
    config.florence_processor = AutoProcessor.from_pretrained("MiaoshouAI/Florence-2-base-PromptGen-v2.0", 
                                                              trust_remote_code=True)
tree = app_commands.CommandTree(client)

def setup_commands():
    group = app_commands.Group(name="aktiva", description="Commands!!!")

    @group.command(name="help", description="Show Aktiva Tutorial")
    async def aktiva_help(interaction: discord.Interaction):
        response = main.show_help()
        await interaction.response.send_message(response, ephemeral=True)

    @group.command(name="list", description="Pull Up A List Of Bots")
    async def aktiva_list(interaction: discord.Interaction):
        response = await main.character_info()
        await interaction.response.send_message(response, ephemeral=True)

    @group.command(name="set_instruction", description="Edit Instruction Data")
    async def aktiva_setinstruction(interaction: discord.Interaction, instruction_desc:str):
        response = main.edit_instruction(interaction,instruction_desc)
        await interaction.response.send_message(response, ephemeral=True)

    @group.command(name="set_global", description="Edit Global Data")
    async def aktiva_setglobal(interaction: discord.Interaction, global_var:str):
        response = main.edit_global(interaction,global_var)
        await interaction.response.send_message(response, ephemeral=True)

    @group.command(name="get_instruction", description="Edit Instruction Data")
    async def aktiva_getinstruction(interaction: discord.Interaction):
        response = main.get_instruction(interaction)
        await interaction.response.send_message(response, ephemeral=True)

    @group.command(name="get_global", description="Edit Global Data")
    async def aktiva_getglobal(interaction: discord.Interaction):
        response = main.get_global(interaction)
        await interaction.response.send_message(response, ephemeral=True)

    @group.command(name="set_whitelist", description="Add Characters, Comma Separated")
    async def aktiva_set_whitelist(interaction: discord.Interaction, character_name:str):
        response = main.set_whitelist(interaction,character_name)
        await interaction.response.send_message(response, ephemeral=True)

    @group.command(name="get_whitelist", description="Show Available Characters")
    async def aktiva_get_whitelist(interaction: discord.Interaction):
        response = main.get_whitelist(interaction)
        await interaction.response.send_message(response, ephemeral=True)

    @group.command(name="clear_whitelist", description="Clear Whitelist")
    async def aktiva_clear_whitelist(interaction: discord.Interaction):
        response = main.clear_whitelist(interaction)
        await interaction.response.send_message(response, ephemeral=True)

    @group.command(name="remove_whitelist", description="Remove a Character")
    async def aktiva_remove_whitelist(interaction: discord.Interaction, character_name:str):
        response = main.delete_whitelist(interaction,character_name)
        await interaction.response.send_message(response, ephemeral=True)

    @group.command(name="set_text_eval_model", description="Change The Model Used to Evaluate Documents")
    async def aktiva_set_eval_model(interaction: discord.Interaction, model_name:str):
        main.change_text_evaluator_model(model_name)
        await interaction.response.send_message("Model Changed!!!\n\nI hope...", ephemeral=True)

    @group.command(name="get_text_eval_model", description="Change The Model Used to Evaluate Documents")
    async def aktiva_get_eval_model(interaction: discord.Interaction):
        await interaction.response.send_message(f"Model is {config.text_evaluator_model}", ephemeral=True)

    @group.command(name="import_character", description="Import a Character JSON file")
    async def aktiva_import_character(interaction: discord.Interaction, character_json: discord.Attachment):
        try:
            # Attempt to process the attachment
            filepath = await fun.save_character_json(character_json)
            await interaction.response.send_message(f"Character imported successfully and saved to: {filepath}", ephemeral=True)
        except ValueError as e:
            # Handle invalid file type errors
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)
        except Exception as e:
            # Catch all other exceptions to avoid crashing
            await interaction.response.send_message(f"An unexpected error occurred: {e}", ephemeral=True)

    @group.command(name="get_pygmalion", description="Import Pygmalion Character")
    async def aktiva_import_pygmalion(interaction: discord.Interaction, character_uuid: str):
        try:
            # Attempt to process the attachment
            filepath = await fun.get_pygmalion_json(character_uuid)
            await interaction.response.send_message(f"{filepath}", ephemeral=True)
        except ValueError as e:
            # Handle invalid file type errors
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)
        except Exception as e:
            # Catch all other exceptions to avoid crashing
            await interaction.response.send_message(f"An unexpected error occurred: {e}", ephemeral=True)

    tree.add_command(group)

@client.event
async def on_ready():
    # Let owner known in the console that the bot is now running!
    print(f'Discord Bot is Loading...')
    config.bot_user = client.user
    # Oh right, I have logging...
    logging.basicConfig(level=logging.DEBUG)

    # Setup the Connection with API
    asyncio.create_task(controller.think())

    # Command to Edit Message (You Right Click On It)
    edit_message = discord.app_commands.ContextMenu(
    name='Edit Bot Message',
    callback=main.edit_message_context,
    type=discord.AppCommandType.message
    )

    # Command to Delete Message (You Right Click On It)
    delete_message = discord.app_commands.ContextMenu(
        name='Delete Bot Message',
        callback=main.delete_message_context,
        type=discord.AppCommandType.message
    )
    
    # Initialize the Commands
    tree.add_command(edit_message)
    tree.add_command(delete_message)
    setup_commands()

    await tree.sync(guild=None)  
    print(f'Discord Bot is up and running.')

@client.event
async def on_message(message):

    if message is None:
        return
    
    # Trigger the Observer Behavior (The command that listens to Keyword)
    print("Message Get")
    await observer.bot_behavior(message, client)

# Run the Bot
client.run(discord_token)
