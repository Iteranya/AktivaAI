import traceback
from duckduckgo_search import AsyncDDGS
from io import BytesIO
from aiohttp import ClientSession
from typing import *
import asyncio
import discord

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

    async def get_image_link(self, max_results: int = 5) -> list:
        
        try:
            # Perform the search using AsyncDDGS
            results = await AsyncDDGS(verify= False).aimages(
                self.query, 
                region='wt-wt',  # worldwide search
                safesearch='off',
                max_results=max_results
            )
            
            # Return the first result if available
            return self.create_embeds(results)
        
        except Exception as e:
            traceback.print_exc()
            print(f"An error occurred during search: {e}")
            return []

    def extract_image_links(self,results):
        # Extract the 'image' URLs from each dictionary in the results list
        links = [result['image'] for result in results if 'image' in result]

        # Join the links with newline characters
        return "\n".join(links)
    
    def create_embeds(self, results):
    # Extract the 'image' URLs from each dictionary in the results list
        embeds = []
        for result in results:
            embed = discord.Embed(description=result['title'], url=result['image'])
            embed.set_image(url=result['image'])  # This line adds the image to the embed
            embeds.append(embed)
        return embeds

    def extract_between_quotes(self,input_string):
        import re
        match = re.search(r"\((.*?)\)", input_string)
        return match.group(1) if match else input_string

    async def download_image(self, url: str):
        """
        Download an image from the given URL and return it as a File object.
        
        Args:
            url (str): URL of the image to download
        
        Returns:
            File: A file-like object containing the image data
        """
        try:
            async with ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        # Read image content
                        image_data = await response.read()
                        
                        # Create a file-like object in memory
                        file = BytesIO(image_data)
                        
                        # Optional: You might want to add more metadata 
                        file.name = url.split('/')[-1]  # Use last part of URL as filename
                        
                        return file
                    else:
                        print(f"Failed to download image from {url}. Status code: {response.status}")
                        return None
        except Exception as e:
            print(f"Error downloading image from {url}: {e}")
            traceback.print_exc()
            return None

    async def get_images(self, max_results: int = 5)-> list:
        """
        Fetch images based on the query and return as a sequence of File objects.
        
        Args:
            max_results (int, optional): Maximum number of images to fetch. Defaults to 5.
        
        Returns:
            Sequence[File]: A list of file-like objects containing image data
        """
        try:
            # Perform the search using AsyncDDGS
            results = await AsyncDDGS(verify=False).aimages(
                self.query, 
                region='wt-wt',  # worldwide search
                safesearch='off',
                max_results=max_results,
            )
            
            # Extract image URLs
            image_urls = [result.get('thumbnail', '') for result in results if result.get('thumbnail')]
            
            # Download images concurrently
            download_tasks = [self.download_image(url) for url in image_urls]
            images = await asyncio.gather(*download_tasks)
            
            # Filter out any None results
            return [img for img in images if img is not None]
        
        except Exception as e:
            print(f"An error occurred during image search: {e}")
            traceback.print_exc()
            return []
