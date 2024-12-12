import re
import config
from duckduckgo_search import AsyncDDGS
from src.discordo import Discordo
from src.aicharacter import AICharacter
from src.dimension import Dimension
from src.prompts import PromptEngineer
from src.llm import LlmApi
from src.models  import QueueItem
from src.multimodal import MultiModal
from src.duckduckgo import Bebek

import traceback
inline_comprehension = True
async def think() -> None:

    while True:
        content = await config.queue_to_process_everything.get()
        discordo:Discordo = content["discordo"]
        bot:AICharacter = content["bot"]
        dimension:Dimension = content["dimension"]
        images = await discordo.process_attachment()
        history = await discordo.initialize_channel_history()
        message_content = discordo.get_user_message_content()
        # if message_content.startswith(">"):
        #     await send_lam_message(bot,discordo,dimension)
        if message_content.startswith("//"):
            pass
        elif message_content.startswith("^"):
            top_result = ""
            image_result = ""
            image_files = None
            bebek = Bebek(message_content)
            if "news" in message_content:
                top_result = await bebek.get_news()
            elif "image" in message_content or "picture" in message_content:
                image_result = await bebek.get_image_link()
                # image_files = await bebek.get_images()
            else:
                top_result = await bebek.get_top_search_result()
            await send_grounded_message(bot,discordo,dimension,str(top_result),image_result)
        elif images:
            if(config.florence):
                multimodal = MultiModal(discordo)
                await send_multimodal_message(bot,discordo,dimension,multimodal)
            else:
                await send_llm_message(bot,discordo,dimension)
        else:
            await send_llm_message(bot,discordo,dimension)
        config.queue_to_process_everything.task_done()


async def send_multimodal_message(bot: AICharacter,discordo: Discordo,dimension:Dimension, multimodal: MultiModal):
        print("Multimodal Processing...")
        image_description = await multimodal.read_image()
        discordo.history+="\n[System Note: User sent the following attachment:"+str(image_description)+"]"

        prompter = PromptEngineer(bot,discordo,dimension)
        queueItem = QueueItem(prompt=await prompter.create_text_prompt())
        llmapi = LlmApi(queueItem,prompter)
        queueItem = await llmapi.send_to_model_queue()
        await discordo.send(bot,queueItem)
        return

async def send_grounded_message(bot: AICharacter,discordo: Discordo,dimension:Dimension,top_message:str,images=None):
    print("Grounding Processing...")
    if top_message!="":
        discordo.history+="\n[System Note: Web Search result: "+top_message+"]"

    print("Chat Completion Processing...")
    prompter = PromptEngineer(bot,discordo,dimension)
    queueItem = QueueItem(prompt=await prompter.create_text_prompt())
    llmapi = LlmApi(queueItem,prompter)
    queueItem = await llmapi.send_to_model_queue()
    queueItem.images = images
    await discordo.send(bot,queueItem)
    return

async def send_llm_message(bot: AICharacter,discordo: Discordo,dimension:Dimension):
    prompter = PromptEngineer(bot,discordo,dimension)
    queueItem = QueueItem(prompt=await prompter.create_text_prompt())
    llmapi = LlmApi(queueItem,prompter)
    print("Chat Completion Processing...")
    queueItem = await llmapi.send_to_model_queue()
    await discordo.send(bot,queueItem)
    return

async def get_top_search_result(query: str, max_results: int = 5) -> dict:
    try:
        # Perform the search using AsyncDDGS
        results = await AsyncDDGS(verify= False).atext(
            query, 
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

async def get_news(query: str, max_results: int = 5) -> dict:
    try:
        # Perform the search using AsyncDDGS
        results = await AsyncDDGS(verify= False).anews(
            query, 
            region='wt-wt',  # worldwide search
            safesearch="off",
            max_results=max_results
            
        )
        return results
    
    except Exception as e:
        traceback.print_exc()
        print(f"An error occurred during search: {e}")
        return {}

async def get_image(query: str, max_results: int = 5) -> dict:
    
    try:
        # Perform the search using AsyncDDGS
        results = await AsyncDDGS(verify= False).aimages(
            query, 
            region='wt-wt',  # worldwide search
            safesearch='off',
            max_results=max_results
        )
        
        # Return the first result if available
        return extract_image_links(results)
    
    except Exception as e:
        traceback.print_exc()
        print(f"An error occurred during search: {e}")
        return {}

def extract_image_links(results):
    # Extract the 'image' URLs from each dictionary in the results list
    links = [result['image'] for result in results if 'image' in result]

    # Join the links with newline characters
    return "\n".join(links)

def extract_between_quotes(input_string):
    import re
    match = re.search(r"\((.*?)\)", input_string)
    return match.group(1) if match else input_string
