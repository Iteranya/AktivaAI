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
            message_content = message_content.replace("^","")
            message_content = message_content.replace(str(bot.name),"")
            message_content = message_content.strip()
            image_result =""
            top_result = ""
            message_content = extract_between_quotes(message_content)
            if "news" in discordo.get_user_message_content():
                top_result = await get_news(message_content)
            elif "image" in discordo.get_user_message_content() or "picture" in discordo.get_user_message_content():
                image_result = await get_image(message_content)
            else:
                top_result = await get_top_search_result(message_content)
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

async def send_grounded_message(bot: AICharacter,discordo: Discordo,dimension:Dimension,top_message:str,images=""):
    print("Grounding Processing...")
    if top_message!="":
        discordo.history+="\n[System Note: Web Search result: "+top_message+"]"
    print("Chat Completion Processing...")
    prompter = PromptEngineer(bot,discordo,dimension)
    queueItem = QueueItem(prompt=await prompter.create_text_prompt())
    llmapi = LlmApi(queueItem,prompter)
    queueItem = await llmapi.send_to_model_queue()
    queueItem.result+="\n"+images
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

# async def send_lam_message(message, json_card):
#     print("LAM Processing...")
#     context = await history.get_channel_history(message.channel)
#     thoughts = "Alright then..."
#     action_bot_prompt = await qutil.get_action_prompt_queue_item(context, thoughts, message, json_card)
#     lam_response = await apiconfig.send_to_model_queue(action_bot_prompt)
#     await lam.process_action(lam_response, message)
#     return


def sanitize_string(input_string):

    sanitized_string = re.sub(r'[^\x00-\x7F]+', '', input_string)
    # Remove unwanted symbols (keeping letters, numbers, spaces, and basic punctuation)
    sanitized_string = re.sub(r'[^a-zA-Z0-9\s.,!?\'\"-]', '', sanitized_string)
    return sanitized_string.strip()

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
