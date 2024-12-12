# This is the function that supports the Observer
import discord
import re
import util
import os
import json


async def get_reply(message: discord.Message, client: discord.Client):
    reply = ""

    # If the message reference is not none, meaning someone is replying to a message
    if message.reference is not None:
        # Grab the message that's being replied to
        referenced_message = message.reference.cached_message
        if referenced_message is None:
            if message.reference.message_id is None:
                print("Message ID is null")
                return reply
            referenced_message = await message.channel.fetch_message(message.reference.message_id)

        # Verify that the author of the message is bot and that it has a reply
        if referenced_message.reference is not None and referenced_message.author == client.user:
            # Grab that other reply as well
            referenced_user_message = referenced_message.reference.cached_message
            if referenced_user_message is None:
                if referenced_message.reference.message_id is None:
                    print("Message ID is null")
                    return reply
                try:
                    referenced_user_message = await message.channel.fetch_message(referenced_message.reference.message_id)
                    # Process the fetched message as needed
                except discord.NotFound:
                    # Handle the case where the message cannot be found
                    print("Message not found or access denied.")
                    return reply

            # If the author of the reply is not the same person as the initial user, we need this data
            if referenced_user_message.author != message.author:
                reply = referenced_user_message.author.display_name + \
                    ": " + referenced_user_message.clean_content + "\n"
                reply = reply + referenced_message.author.display_name + \
                    ": " + referenced_message.clean_content + "\n"
                reply = util.clean_user_message(reply)

                return reply

        # If the referenced message isn't from the bot, use it in the reply
        if referenced_message.author != client.user:
            reply = referenced_message.author.display_name + \
                ": " + referenced_message.clean_content + "\n"

            return reply

    return reply


def get_user_list(history: str) -> list[str]:
    # Define the regex pattern
    pattern = r'(?<=\n)[\w-]+(?=:)'
    
    # Find all matches using the regex pattern
    matches = re.findall(pattern, history, flags=re.MULTILINE)
    
    # Convert the list of matches to a set to remove duplicates
    unique_usernames = [username for username in set(matches)]
    
    # Convert the set back to a sorted list (if sorting is needed)
    return sorted(list(unique_usernames))

def get_replied_user(reply: str) -> list[str]:
    pattern = r'[\w-]+(?=:)'
    matches = re.findall(pattern, reply, flags=re.MULTILINE)
    
    # Convert the list of matches to a set to remove duplicates
    unique_usernames = [username for username in set(matches)]
    # Convert the set back to a sorted list (if sorting is needed)
    return sorted(list(unique_usernames))

async def get_bot_list() -> list[str]:
    names = []
    folder_path = "./characters"
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
                    if name:
                        names.append(name)
                    else:
                        pass
                except json.JSONDecodeError as e:
                    print(f"Error parsing {filename}: {e}")

    return names

async def get_bot_whitelist(channel_name:str) -> list[str]:
    names = []
    folder_path = "./characters"
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
                    whitelist = data.get('whitelist',None)
                    if whitelist!=None:
                        if channel_name in whitelist:
                            names.append(data.get('name'))
                        else:
                            pass
                    else:
                        name = data.get('name')
                        if name:
                            names.append(name)
                        else:
                            pass
                except json.JSONDecodeError as e:
                    print(f"Error parsing {filename}: {e}")

    return names

async def get_channel_whitelist(channel_name:str) -> list[str]:
    names = []
    folder_path = "./channels"
    # Iterate over each file in the directory
    file_path = os.path.join(folder_path, channel_name+".json")
    if channel_name.endswith('.json'):
        # Read the JSON file
        with open(file_path, 'r') as f:
            try:
                # Load JSON data
                data = json.load(f)
                # Extract the name field and append to names list
                whitelist = data.get('whitelist',None)
                return whitelist
            except json.JSONDecodeError as e:
                print(f"Error parsing {channel_name}: {e}")

    return names

