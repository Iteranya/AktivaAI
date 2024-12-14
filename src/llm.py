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

class LlmApi:
    def __init__(self, queue:QueueItem, prompt_engineer:PromptEngineer, inline=True):
        self.queue = queue
        self.prompt_engineer = prompt_engineer
        self.inline_comprehension = inline
        self.text_api = prompt_engineer.api

    async def send_to_model_queue(self)->QueueItem:
        # Get the queue item that's next in the list
        timeout = ClientTimeout(total=600)
        connector = TCPConnector(limit_per_host=10)
        async with ClientSession(timeout=timeout, connector=connector) as session:
            try:
                async with session.post(self.text_api["address"] + self.text_api["generation"], headers=self.text_api["headers"], data=self.queue.prompt) as response:
                    if response.status == 200:
                        try:
                            json_response = await response.json()
                            print("Json Responsse Get")
                            llm_response:str = self.clean_up(json_response)
                            self.queue.result = llm_response
                            return self.queue
                        except json.decoder.JSONDecodeError as e:
                            # Handle the case where response is not JSON-formatted
                            return await self.handle_error_response(e)
                    else:
                        # Handle non-200 responses here
                        print(f"HTTP request failed with status: {response.status}")
                        return await self.handle_error_response(response.status)

            except Exception as e:
                # Handle any other exceptions
                return await self.handle_error_response(e)

    async def handle_error_response(self,e: Exception) -> None:
        self.queue.error = "Bot's asleep, probably~ \nHere's the error code:" +str(e)
        return self.queue
    

    def clean_up(self,llm_response: dict[str, Any]) -> None:
        try:
            data = llm_response['results'][0]['text']
        except KeyError:
            data = llm_response['choices'][0]['message']['content']

        if not data:
            return
        cleaned_data:str = textutil.remove_last_word_before_final_colon(data)
        cleaned_data = textutil.remove_string_before_final(cleaned_data)
        cleaned_data = cleaned_data.strip()
        if cleaned_data.endswith("*.") or cleaned_data.endswith("*"):
            if random.choice([True, False]):  # 50/50 chance
                cleaned_data = textutil.remove_fluff(cleaned_data)
        cleaned_data = textutil.clean_text(cleaned_data)
        llm_message = cleaned_data
        
        return llm_message

    
