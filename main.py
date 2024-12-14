import json
import os
import discord
import config
import re
import traceback

client = config.client

class EditMessageModal(discord.ui.Modal, title='Edit Message'):
    def __init__(self, original_message):
        super().__init__()
        self.original_message:discord.Message = original_message
        print(original_message)

        # Set the default value of the TextInput to the content of the original message
        self.new_content = discord.ui.TextInput(
            label='New Content', 
            style=discord.TextStyle.long, 
            required=True, 
            default=self.original_message.content
        )
        # Add the TextInput to the modal
        self.add_item(self.new_content)

    async def on_submit(self, interaction: discord.Interaction):
        thread = None
        try:
            try:
                self.original_message = await self.original_message.channel.fetch_message(self.original_message.id)
            except discord.NotFound:
                print(f"Message ID {self.original_message.id} not found in thread {self.original_message.channel.name}.")
                await interaction.response.send_message("The original message was not found in this thread.", ephemeral=True)
                return
            # Fetch the webhook associated with the original message
            if isinstance(self.original_message.channel,discord.Thread):
                webhooks = await self.original_message.channel.parent.webhooks()
                thread  = self.original_message.channel
            else:
                webhooks = await self.original_message.channel.webhooks()
            webhook = next((hook for hook in webhooks if hook.id == self.original_message.webhook_id), None)

            if not webhook:
                await interaction.response.send_message("Webhook not found for this message.", ephemeral=True)
                return
            print("ORIGINAL MESSAGE:")
            print(self.original_message.id)
            print(self.new_content.value)
            # Edit the message using the webhook
            if thread is not None:
                await webhook.edit_message(
                    message_id=self.original_message.id,
                    content=self.new_content.value,
                    thread = thread
                )
            else:
                await webhook.edit_message(
                    message_id=self.original_message.id,
                    content=self.new_content.value,
                )
            await interaction.response.send_message("Message edited successfully!", ephemeral=True)
        except discord.NotFound:
            traceback.print_exc()
            await interaction.response.send_message("The original message was not found.", ephemeral=True)
        except Exception as e:
            traceback.print_exc()
            await interaction.response.send_message("An error occurred while editing the message.", ephemeral=True)
    # async def on_submit(self, interaction: discord.Interaction):
    #     await edit(self.original_message, self.new_content.value)
    #     await interaction.response.send_message("Message edited successfully!", ephemeral=True)

def edit_instruction(interaction: discord.Interaction, message: str):
    data = createOrFetchJson(interaction.channel.name)
    data["instruction"] =  message
    replaceJsonContent(interaction.channel.name,data)
    return data["instruction"]

def get_instruction(interaction: discord.Interaction):
    data = createOrFetchJson(interaction.channel.name)
    return data["instruction"]

def edit_global(interaction: discord.Interaction, message: str):
    data = createOrFetchJson(interaction.channel.name)
    data["global"] =  message
    replaceJsonContent(interaction.channel.name,data)
    return data["global"]

def get_global(interaction: discord.Interaction):
    data = createOrFetchJson(interaction.channel.name)
    return data["global"]

def add_whitelist(interaction: discord.Interaction, character_name: str):
    # Fetch or create the JSON data
    data = createOrFetchJson(interaction.channel.name)

    # Initialize the "whitelist" key if it doesn't exist
    if "whitelist" not in data:
        data["whitelist"] = []

    # Add the character to the whitelist if not already present
    if character_name not in data["whitelist"]:
        data["whitelist"].append(character_name)
        replaceJsonContent(interaction.channel.name,data)
    return data["whitelist"]

def clear_whitelist(interaction: discord.Interaction):
    # Fetch or create the JSON data
    data = createOrFetchJson(interaction.channel.name)
    
    # Clear the whitelist
    data["whitelist"] = []
    replaceJsonContent(interaction.channel.name, data)
    return data["whitelist"]

def set_whitelist(interaction: discord.Interaction, whitelist_string: str):
    # Fetch or create the JSON data
    data = createOrFetchJson(interaction.channel.name)
    
    # Split the string by comma and strip whitespace
    whitelist = [name.strip() for name in whitelist_string.split(',')]
    
    # Set the whitelist
    data["whitelist"] = whitelist
    replaceJsonContent(interaction.channel.name, data)
    return data["whitelist"]

def delete_whitelist(interaction: discord.Interaction, character_name: str):
    # Fetch or create the JSON data
    data = createOrFetchJson(interaction.channel.name)
    
    # Remove the character from the whitelist if present
    if "whitelist" in data and character_name in data["whitelist"]:
        data["whitelist"].remove(character_name)
        replaceJsonContent(interaction.channel.name, data)
    
    return data["whitelist"]

def get_whitelist(interaction: discord.Interaction):
    # Fetch or create the JSON data
    data = createOrFetchJson(interaction.channel.name)
    
    # Return the whitelist, defaulting to an empty list if not present
    return data.get("whitelist", [])

async def delete_message_context(interaction: discord.Interaction, message: discord.Message):
    await delete(message,interaction)

async def edit_message_context(interaction: discord.Interaction, message: discord.Message):
    if message.webhook_id!=None:
        await client.fetch_webhook(message.webhook_id)
        await interaction.response.send_modal(EditMessageModal(message))
    await interaction.response.send_message("This isn't a bot's message, this is human's message")

async def edit(message:discord.Message, webhook_id, new_content):
    print(webhook_id)
    webhook = await client.fetch_webhook(webhook_id)
    await webhook.edit_message(message_id=message.id,content=new_content)

async def delete(message:discord.Message,interaction:discord.Interaction):
    webhook = await client.fetch_webhook(message.webhook_id)
    if isinstance(interaction.channel,discord.Thread):
        await webhook.delete_message(message.id,thread=interaction.channel)
    else:
        await webhook.delete_message(message.id)
    await interaction.response.send_message("Deleted~")

async def character_info():
    character = await get_bot()
    result_str = "\n".join([f"{name}: {info}" for name, info in character.items()])
    return result_str

async def get_bot():
    folder_path = "./characters"
    bot_dict = {}  # Dictionary to store bot name and info

    # Iterate over each file in the directory
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.endswith('.json'):
            # Read the JSON file
            with open(file_path, 'r') as f:
                try:
                    # Load JSON data
                    data = json.load(f)
                    # Extract the name field and append to names list
                    name = data.get('name')
                    info = data.get('info')
                    if name and info:
                        # Put the bot name and info in a dictionary
                        bot_dict[name] = info
                except json.JSONDecodeError as e:
                    print(f"Error parsing {filename}: {e}")

    return bot_dict



# Well Fuck, I need to redo the memory first!!!

def createOrFetchJson(input_string):
    # File name with .json extension
    file_name = f"channels/{input_string}.json"

    # Check if the file already exists
    if os.path.exists(file_name):
        # Open and fetch the content
        with open(file_name, "r") as json_file:
            data = json.load(json_file)
        print(f"File '{file_name}' already exists. Fetched content: {data}")
        return data
    
    # If it doesn't exist, create the data and save it
    data = {
        "name": input_string,
        "description":"[System Note: Takes place in a discord text channel]",
        "global":"[System Note: Takes place in a discord server]",
        "instruction":"[System Note: Takes place in a discord text channel]"
        }
    with open(file_name, "w") as json_file:
        json.dump(data, json_file, indent=4)
    print(f"File '{file_name}' created with content: {data}")
    return data

def replaceJsonContent(file_name, new_content):
    """Replaces the content of the JSON file with a given dictionary."""
    # Ensure the file name ends with .json
    if not file_name.endswith(".json"):
        file_name += ".json"
    
    # Check if the file exists
    if not os.path.exists("channels/"+file_name):
        print(f"File '{file_name}' does not exist. Cannot replace content.")
        return None

    # Ensure new_content is a dictionary
    if not isinstance(new_content, dict):
        raise ValueError("New content must be a dictionary.")

    # Replace the content
    with open("channels/"+file_name, "w") as json_file:
        json.dump(new_content, json_file, indent=4)
    print(f"File '{file_name}' content replaced with: {new_content}")
    return new_content

def sanitize_string(input_string):

    sanitized_string = re.sub(r'[^\x00-\x7F]+', '', input_string)
    # Remove unwanted symbols (keeping letters, numbers, spaces, and basic punctuation)
    sanitized_string = re.sub(r'[^a-zA-Z0-9\s.,!?\'\"-]', '', sanitized_string)
    return sanitized_string.strip()
