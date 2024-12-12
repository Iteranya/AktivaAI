import discord
import config
import src.textutil as textutil
import os
import json

class AICharacter:
    def __init__(self, bot_name:str):
        self.bot_name = bot_name
        self.char_dict = self.get_card(bot_name)
        self.name:str = self.char_dict["name"]
        self.persona:str = self.char_dict["persona"]
        self.examples:list = self.char_dict["examples"]
        self.instructions:str = self.char_dict["instructions"]
        self.avatar:str = self.char_dict["image"]
        self.info:str = self.char_dict["info"]

    def getDictFromJson(self,json_path):
        with open(json_path, 'r') as f:
            try:
                # Load JSON data
                data = json.load(f)
                return data

            except json.JSONDecodeError as e:
                print(f"Error parsing {json_path}: {e}")
        return None
    
    def saveDictToJson(self):
        data = self.char_dict
        json_path = f"../characters/{self.bot_name}.json"
        try:
            with open(json_path, 'w') as f:
                # Save the dictionary as JSON
                json.dump(data, f, indent=4)
                print(f"Successfully saved data to {json_path}")
        except TypeError as e:
            print(f"Error saving data to {json_path}: {e}")
        except IOError as e:
            print(f"I/O error occurred while writing to {json_path}: {e}")

    def get_card(self,bot_name: str):
        directory = "./characters"
        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                filepath = os.path.join(directory, filename)
                try:
                    # Open and load JSON file
                    with open(filepath, 'r', encoding='utf-8') as file:
                        data = json.load(file)

                    # Check if 'name' field matches target_name
                    if "name" in data and str(data["name"]).lower() == str(bot_name).lower():
                        return data
                except json.JSONDecodeError:
                    print(f"Error decoding JSON in file: {filepath}")
                except Exception as e:
                    print(f"Error processing file {filepath}: {e}")

    async def get_character_prompt(self) -> str | None:
        # Your name is <name>.
        character: str = "You are " + self.name + ", you embody their character, persona, goals, personality, and bias which is described in detail below:"

        # Your name is <name>. You are a <persona>.
        character = character + "Your persona: " + self.persona + ". "

        # Instructions on what the bot should do. This is where an instruction model will get its stuff.

        examples = self.examples  # put example responses here

        for example in examples:
            if example.startswith("[System"):
                pass
            else:
                example = f"[Reply] {example}"

        # Example messages!
        character_prompt = character + " A history reference to your speaking quirks and behavior: " + \
        "\n" + '\n'.join(examples) + "\n"

        return character_prompt




    def get_name(self) -> str:
        """Getter for character name."""
        return self.name

    def get_persona(self) -> str:
        """Getter for character persona."""
        return self.persona

    def get_examples(self) -> list:
        """Getter for character examples."""
        return self.examples

    def get_instructions(self) -> str:
        """Getter for character instructions."""
        return self.instructions

    def get_avatar(self) -> str:
        """Getter for character avatar."""
        return self.avatar

    def get_info(self) -> str:
        """Getter for character info."""
        return self.info

    def get_json_path(self) -> str:
        """Getter for JSON file path."""
        return self.json_path

    # Setters
    def set_name(self, name: str):
        """Setter for character name."""
        self.name = name
        self.char_dict["name"] = name

    def set_persona(self, persona: str):
        """Setter for character persona."""
        self.persona = persona
        self.char_dict["persona"] = persona

    def set_examples(self, examples: list):
        """Setter for character examples."""
        self.examples = examples
        self.char_dict["examples"] = examples

    def set_instructions(self, instructions: str):
        """Setter for character instructions."""
        self.instructions = instructions
        self.char_dict["instructions"] = instructions

    def set_avatar(self, avatar: str):
        """Setter for character avatar."""
        self.avatar = avatar
        self.char_dict["image"] = avatar

    def set_info(self, info: str):
        """Setter for character info."""
        self.info = info
        self.char_dict["info"] = info
    

    


   
    


