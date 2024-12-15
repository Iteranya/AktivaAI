import json
import re
from aiohttp import ClientSession
from aiohttp import ClientTimeout
from aiohttp import TCPConnector

from aiohttp import ClientSession
from aiohttp import ClientTimeout
from aiohttp import TCPConnector
import random
from typing import Any
import util
import src.textutil as textutil
from src.models import QueueItem
from src.discordo import Discordo
from src.aicharacter import AICharacter
from src.dimension import Dimension
from src.prompts import PromptEngineer
import config
from openai import OpenAI

class LlmApi:
    def __init__(self, queue: QueueItem, prompt_engineer: PromptEngineer, inline=True):
        self.queue = queue
        self.prompt_engineer = prompt_engineer
        self.inline_comprehension = inline
        self.text_api = prompt_engineer.api
        self.model_type = prompt_engineer.type  # Store the model type

    async def send_to_model_queue(self) -> QueueItem:
        timeout = ClientTimeout(total=600)
        connector = TCPConnector(limit_per_host=10)
        async with ClientSession(timeout=timeout, connector=connector) as session:
            try:
                if self.model_type == "local":
                    async with session.post(self.text_api["address"] + self.text_api["generation"], headers=self.text_api["headers"], data=self.queue.prompt) as response:
                        if response.status == 200:
                            try:
                                json_response = await response.json()
                                llm_response: str = self.clean_up(json_response)
                                self.queue.result = llm_response
                                return self.queue
                            except json.decoder.JSONDecodeError as e:
                                return await self.handle_error_response(e)
                        else:
                            print(f"HTTP request failed with status: {response.status}")
                            return await self.handle_error_response(response.status)

                elif self.model_type == "openrouter":
                    try:
                        openai = OpenAI(
                            base_url="https://openrouter.ai/api/v1",
                            api_key=config.openrouter_token,  # Replace with your actual key
                        )
                        #print(self.queue.prompt)
                        # Convert the JSON string to a Python dictionary
                        prompt_dict = json.loads(self.queue.prompt)
                        # Extract the prompt string
                        prompt_string = prompt_dict['prompt']
                        completion = await openai.chat.completions.create(
                            model="meta-llama/llama-3.1-70b-instruct:free",
                            messages=[{"role": "user", "content": prompt_string}]
                        )
                        self.queue.result = completion.choices[0].message.content
                        return self.queue

                    except Exception as e:
                        print(f"OpenAI API Error: {e}")
                        return await self.handle_error_response(e)
                else:
                    raise ValueError(f"Unsupported model type: {self.model_type}")

            except Exception as e:
                return await self.handle_error_response(e)

    async def handle_error_response(self, e: Exception) -> QueueItem: #Added typehint
        self.queue.error = "Bot's asleep, probably~ \nHere's the error code:" + str(e)
        return self.queue

    def clean_up(self, llm_response: dict[str, Any]) -> str:
        try:
            data = llm_response['results'][0]['text']
        except KeyError:
            try:
                data = llm_response['choices'][0]['message']['content']
            except KeyError:
                return "" # Return empty string if no data found.

        if not data:
            return ""

        cleaned_data: str = textutil.remove_last_word_before_final_colon(data)
        cleaned_data = textutil.remove_string_before_final(cleaned_data)
        cleaned_data = cleaned_data.strip()
        if cleaned_data.endswith("*.") or cleaned_data.endswith("*"):
            if random.choice([True, False]):  # 50/50 chance
                cleaned_data = textutil.remove_fluff(cleaned_data)
        cleaned_data = textutil.clean_text(cleaned_data)
        llm_message = cleaned_data

        return llm_message
    
