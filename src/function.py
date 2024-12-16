# This is the function that supports the Observer
import discord
import re
import util
import os
import json
import aiohttp
import src.filemanager as filemanager

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
                    card_data = data.get('data')
                    name  = data.get('name')
                    if name:
                        names.append(name)
                    elif card_data:
                        name = card_data.get("name")
                        if name:
                            names.append(name)
                        else:
                            pass
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

async def get_channel_whitelist(channel_name: str) -> list[str] | None:
    file_path = f"./channels/{channel_name}.json"

    # Check if the file exists
    if not os.path.exists(file_path):
        return None

    # Attempt to read and parse the JSON file
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            # Extract the 'whitelist' field, if present
            return data.get('whitelist', None)
    except json.JSONDecodeError as e:
        print(f"Error parsing {channel_name}: {e}")

    return None


async def save_character_json(attachment: discord.Attachment) -> str:
    """
    Save a Discord attachment, extracting JSON if it's a PNG with embedded metadata.

    Args:
        attachment (discord.Attachment): The Discord attachment to process

    Returns:
        str: Descriptive string about the processing result
    """
    # Create the attachments directory if it doesn't exist
    attachments_dir = os.path.join(os.getcwd(), 'characters')

    # Generate the base filepath
    filename: str = attachment.filename
    
    # Handle JSON files
    if filename.lower().endswith(".json"):
        filepath = os.path.join(attachments_dir, filename)
        
        # Check if the file already exists
        if os.path.exists(filepath):
            return f"JSON file {filename} already exists"

        # Save the new attachment
        with open(filepath, 'wb') as f:
            attachment_bytes = await attachment.read()
            f.write(attachment_bytes)

        return f"JSON file {filename} saved"

    # # Handle PNG files
    # if filename.lower().endswith(".png"):
    #     filepath = os.path.join(attachments_dir, filename)
        
    #     # Check if the file already exists
    #     if os.path.exists(filepath):
    #         try:
    #             # Attempt to extract JSON if the PNG exists
    #             return filemanager.png_to_json(filepath)
    #         except ValueError:
    #             return f"PNG file {filename} already exists, no JSON found"

    #     # Save the new attachment
    #     with open(filepath, 'wb') as f:
    #         attachment_bytes = await attachment.read()
    #         f.write(attachment_bytes)

    #     # Try to extract JSON after saving
    #     try:
    #         return filemanager.png_to_json(filepath)
    #     except ValueError:
    #         return f"PNG file {filename} saved, no JSON found"
    
    # If not a PNG or JSON
    return f"Unsupported file type: {filename}"

async def get_pygmalion_json(uuid:str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=f"https://server.pygmalion.chat/api/export/character/{uuid}/v2",
                headers={
                    "Content-Type": "application/json"
                }
            ) as response:
                # Raise exception for bad HTTP status
                response.raise_for_status()
                result = await response.json()
                print(str(result))
                if result.get('character',None)!=None:
                    try:
                        data = result['character']
                        filename = f"characters/{result['character']['data']['name']}.json"
                        with open(filename, 'w') as file:
                            json.dump(data, file, indent=4)
                        return f"Dictionary successfully saved to {filename}"
                    except Exception as e:
                        print(f"An error occurred: {e}")
                        return print(f"An error occurred: {e}")
                else:
                    return f"Error Reading File: {result['error']['message']}, Notify User That An Error Occured."
    except aiohttp.ClientError as e:
        print(f"Network error in LLM evaluation: {e}")
    except (KeyError, ValueError) as e:
        print(f"Parsing error in LLM response: {e}")
    except Exception as e:
        print(f"Unexpected error in LLM evaluation: {e}")
    return None
