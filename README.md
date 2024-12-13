# Aktiva AI - A Self Hosted AI Discord Bot

## FEATURES!!!

### Seamless Character Swapping
- You only need to say a character's name or answer to their reply to trigger them!
- /list to get the list of all available characters!!!
- Call upon her name, 'Aktiva-chan' for the default built in AI that can explain how the Bot Works!!!
- Use double slash `//` in the beginning of your message to hide it from the AI and context (the emoji still appears, but it won't reply)
- All characters uses Webhooks! So different avatar for different name~ 
- Adding character is as easy as making a json and putting them in the characters folder! (refer to character MD file please)

### Channel Thread Memory and Location
- Use slash command to manipulate Memory and Location
- Memory is located before history context, location is located after history context
- Each channel and thread has its own memory and location!!!
- YES SUPPORTS THREADS!!! WOOOOOOOOOOOOOOOOO!!!!!
- Get yourself a nice private thread with your own AI!!!
- Mitochondria is the powerhouse of cell

### Stable Multi-line Support
- Uses some epic prompt enginneering to keep the AI stable (not that epic actually)
- If character is made in the correct format, the AI shouldn't hallucinate much outside of their character
- Supports both Assistant mode and Roleplay mode!!!
- Can add line breaks, yes, ask your AI to write things past discord word limit too!
- Very stable, no need to worry about the AI impersonating you!
  
### Image Recognition
- Uses the the finetune of Microsoft's Florence 2 AI [MiaoshouAI/Florence-2-base-PromptGen-v2.0](https://huggingface.co/MiaoshouAI/Florence-2-base-PromptGen-v2.0) for object recognition
- ~~Uses Llava by default for vibe detection~~ Optional!!! Because not all LLM are Multimodal
- Combined, this puppy can *almost* beat most Open Source Image detection out there! Recognizing the object and getting the vibe and aesthetic at the same time!

### Character Text Edit and Deletion
- Yes! You can edit your character's response like it's SillyTavern
- Yes! You can delete your character's response!
- No! You cannot regenerate character's response, I should really add that feature

## Prerequisites

### Large Language Model
If you want to be cultured, you'll also need to download one of these bad boys~

- [Stheno - One of the best Llama 8B Model](https://huggingface.co/Lewdiculous/L3-8B-Stheno-v3.1-GGUF-IQ-Imatrix) <- The Most Stable One Yet
- [Nyanade - One of the best Llama 7B Model](https://huggingface.co/Lewdiculous/Nyanade_Stunna-Maid-7B-v0.2-GGUF-IQ-Imatrix) <- 7B Model, Use At Your Own Risk

### Koboldcpp
Requires Koboldcpp for back end, download it here:
[Koboldcpp](https://github.com/LostRuins/koboldcpp)

### Florence 2 Finetune

- Microsoft New Visual AI
- Finetuned to detect character appearance and image composition
- Text Recognition too!!
 
### Additional configuration needed to run the bot
- Discord API key in .env in the global variable
- make new character json files in the characters folder
- Or just, yknow, make lots and lots of character json file!!! Refer to characters/default.json for example


## Instructions:

To run this bot:

1. Load the LLM model of your choice in Koboldcpp (Make sure it's marked as not safe for audience)
2. Download this repository [Aktiva AI](https://github.com/Iteranya/AktivaAI/)
3. Make a .env file as written in example.env
4. Install the requirements. I suggest using an Anaconda or Miniconda instance.
    ```pip install -r requirements.txt```
5. Run the bot with `python bot.py`

## Character creation

Refer to README.md file in the characters folder.

## ToDo (From Top Priority to the Least Important):

- [x] Make a better README.
- [x] Add Webhook Support for more seamless Avatar Change
- [x] Fixed the Webhook not detecting reply, (hopefully I don't get rate limited)
- [x] Refactor this whole entire mess...
- [x] Redo the character trigger and swapping system with webhook.
- [x] Implement GBNF for literal fucking Large Action Model feature.
- [ ] [Add a nicer way to add the Large Action Model Feature](https://huggingface.co/facebook/bart-large-mnli)
- [ ] Refactor this whole entire mess... AGAIN!!!

## Known Issue:
- Terrible Documentation
  - As in like, I did not make any proper Github Commit Comment :v
  - Honestly this whole thing started as a joke, if you see the Read Me file, it's all just irony
  - I never expected it to work this well

Yeah that's all the current issue. Let me know if there's another one, have fun then~

## Credits!

- Big thank you to @badgids for the fork (even though this has no resemblance to the original)\
- All the Beta Tester at Ambruk Academy Discord Server
- You <3

