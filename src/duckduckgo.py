import traceback
import discord.types
import discord.types.embed
from duckduckgo_search import AsyncDDGS
from io import BytesIO
from aiohttp import ClientSession
from typing import *
import asyncio
import discord
import config

class Bebek:
    def __init__(self, query:str, inline=True):
        self.query = self.extract_between_quotes(query)

    async def get_top_search_result(self, max_results: int = 5) -> dict:
        try:
            # Perform the search using AsyncDDGS
            results = await AsyncDDGS(verify= False).atext(
                self.query, 
                region='wt-wt',  # worldwide search
                safesearch="off",
                max_results=max_results
                
            )
            
            # Return the first result if available
            return results
        
        except Exception as e:
            traceback.print_exc()
            print(f"An error occurred during search: {e}")
            return {}

    async def get_news(self, max_results: int = 5) -> dict:
        try:
            # Perform the search using AsyncDDGS
            results = await AsyncDDGS(verify= False).anews(
                self.query, 
                region='wt-wt',  # worldwide search
                safesearch="off",
                max_results=max_results
                
            )
            return results
        
        except Exception as e:
            traceback.print_exc()
            print(f"An error occurred during search: {e}")
            return {}

    async def get_image_link(self, safesearch:str = 'off',max_results: int = 5) -> list:

        try:
            # Perform the search using AsyncDDGS
            results = await AsyncDDGS(verify= False).aimages(
                self.query, 
                region='wt-wt',  # worldwide search
                safesearch=safesearch,
                max_results=max_results
            )
            
            # Return the first result if available
            return self.create_embeds(results)
        
        except Exception as e:
            traceback.print_exc()
            print(f"An error occurred during search: {e}")
            return []
        
    async def get_video_link(self, max_results: int = 5) -> str:
        
        try:
            # Perform the search using AsyncDDGS
            results = await AsyncDDGS(verify= False).avideos(
                self.query, 
                region='wt-wt',  # worldwide search
                safesearch='off',
                max_results=max_results
            )
            
            # Return the first result if available
            return self.extract_links(results)
        
        except Exception as e:
            traceback.print_exc()
            print(f"An error occurred during search: {e}")
            return []

    def extract_links(self,results):
        # Extract the 'image' URLs from each dictionary in the results list
        links = ["[.]("+result['content']+")" for result in results if 'content' in result]

        # Join the links with newline characters
        return " ".join(links)
    
    def create_embeds(self, results, media_type='image'):
        embeds = []
        for result in results:
            if media_type == 'image':
                embed = discord.Embed(description=result['title'], url=result['image'])
                embed.set_image(url=result['image'])
            elif media_type == 'video':
                embed = discord.Embed(title=result['title'],description=result['content'], url=result['content'],type='video')
            else:
                raise ValueError("media_type must be 'image' or 'video'")
            
            embeds.append(embed)
        return embeds

    def extract_between_quotes(self,input_string):
        import re
        match = re.search(r"\((.*?)\)", input_string)
        return match.group(1) if match else input_string
