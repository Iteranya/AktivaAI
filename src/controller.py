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
        try:
            await discordo.raw_message.add_reaction('✨')
        except Exception as e:
            print("Hi!")
        images = await discordo.process_attachment()
        history = await discordo.initialize_channel_history()
        message_content = discordo.get_user_message_content()
        # if message_content.startswith(">"):
        #     await send_lam_message(bot,discordo,dimension)
        if message_content.startswith("//"):
            pass
        elif message_content.startswith("^"):
            top_result = ""
            image_result = None
            bebek = Bebek(message_content)
            if "news" in message_content:
                top_result = await bebek.get_news()
            elif "image" in message_content or "picture" in message_content:
                image_result = await bebek.get_image_link()
                
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
        if config.immersive_mode:
            discordo.history+="\n[System Note: User sent the following attachment:"+str(image_description)+"]"
        else:
            discordo.send_as_user("[System Note: User sent the following attachment:"+str(image_description)+"]")
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
