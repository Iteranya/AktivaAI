# Clutters I don't wanna put in the function

import json
import os
import re
import base64
from PIL import Image
from typing import Any
import io
import datetime
from pathlib import Path
import shutil

def clean_user_message(user_input: str) -> str:
    # Remove the bot's tag from the input since it's not needed.
    user_input = user_input.replace("@Kobold", "")

    user_input = user_input.replace("<|endoftext|>", "")

    # Remove any spaces before and after the text.
    user_input = user_input.strip()

    return user_input

# Mistral-medium hallucinates some stuff in parentheses on newlines and then it hallucinates more
def truncate_from_newline_parenthesis(text: str) -> str:
    # This regex pattern matches an open parenthesis at the start of any line within the text
    pattern = r'^\('

    # Use the MULTILINE flag to ensure ^ matches the start of each line
    match = re.search(pattern, text, re.MULTILINE)

    # If a match is found, return the substring up to that point, else return the original string
    if match:
        return text[:match.start()]
    else:
        return text

def encode_image_to_base64(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode('utf-8')

async def convert_webp_bytes_to_png(image_bytes: bytes) -> bytes:
    with io.BytesIO(image_bytes) as image_file:
        with Image.open(image_file) as img:
            output_buffer = io.BytesIO()
            img.save(output_buffer, format="PNG")
            return output_buffer.getvalue()

def get_file_name(directory: str, file_name: str) -> str:
    # Create the file path from name and directory and return that information
    filepath = os.path.join(directory, file_name)
    return filepath

# Read in a JSON file and spit it out, usefully or "None" if file's not there or we have an issue
def clean_username(username: str) -> str:
    # Replace invalid characters with an underscore
    cleaned_username = re.sub(r'[<>:"/\\|?*]', '_', username)

    # Remove any trailing spaces or periods (as they are not allowed at the end of Windows filenames)
    cleaned_username = cleaned_username.rstrip('. ')
    return cleaned_username

def get_json_file(filename: str) -> dict[str, Any] | None:
    # Try to go read the file!
    try:
        with open(filename, 'r') as file:
            contents = json.load(file)
            return contents
    # Be very sad if the file isn't there to read
    except FileNotFoundError:
        # await write_to_log("File " + filename + "not found. Where did you lose it?")
        return None
    # Be also sad if the file isn't a JSON or is malformed somehow
    except json.JSONDecodeError:
        # await write_to_log("Unable to parse " + filename + " as JSON.")
        return None
    # Be super sad if we have no idea what's going on here
    except Exception as e:
        #await write_to_log(f"An unexpected error occurred: {e}")
        return None

# Write a line to the log file
async def write_to_log(information: str) -> None:
    file = get_file_name("", "log.txt")

    # Add a time stamp to the provided error message
    current_time = datetime.datetime.now()
    rounded_time = current_time.replace(microsecond=0)
    text = str(rounded_time) + " " + information + "\n"

    await append_text_file(file, text)

async def append_text_file(file: str, text: str) -> None:

    with open(file, 'a+', encoding="utf-8") as context:
        context.write(text)
        context.close()

def get_file_list(directory: str) -> list[str]:
    # Try to get the list of character files from the directory provided.
    try:
        dir_path = directory + "\\"
        files = os.listdir(dir_path)
    except FileNotFoundError:
        files = []
    except OSError:
        files = []

    # Return either the list of files or a blank list.
    return files

def initialize_data_directories():
    """
    Copy data files from initial_data to their respective directories.
    Creates directories if they don't exist and copies all files from initial_data.
    """
    # Define the directories we need
    data_dirs = ['characters', 'attachments', 'configurations']
    base_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    
    # Process each directory
    for dir_name in data_dirs:
        # Create target directory if it doesn't exist
        target_dir = base_dir / dir_name
        target_dir.mkdir(exist_ok=True)
        
        # Path to initial data
        initial_data_dir = base_dir / 'initial_data' / dir_name
        
        if initial_data_dir.exists():
            print(f"Copying files for {dir_name}...")
            # Copy all files from initial_data directory
            for file in initial_data_dir.glob('*'):
                shutil.copy2(file, target_dir / file.name)
                print(f"Copied {file.name} to {dir_name}/")
        else:
            print(f"Warning: No initial data found for {dir_name} at {initial_data_dir}")
