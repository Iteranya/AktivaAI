# Aktiva AI - A Self-Hosted AI Discord Bot
Your digital companion for managing and interacting with multiple AI personalities on Discord.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
    - [Seamless Character Swapping](#seamless-character-swapping)
    - [Channel-Based Memory](#channel-based-memory)
    - [Thread Support](#thread-support)
    - [Image Recognition](#image-recognition)
    - [Character Message Editing and Deletion](#character-message-editing-and-deletion)
    - [Customizable AI Characters](#customizable-ai-characters)
    - [PDF File Reading Support](#pdf-file-reading-support)
    - [Web Search Integration](#web-search-integration)
    - [Whitelist Management](#whitelist-management)
    - [OpenRouter API Integration](#openrouter-api-integration)
    - [SillyTavern Character Compatibility](#sillytavern-character-compatibility)
3. [Prerequisites](#prerequisites)
4. [Installation Guide](#installation-guide)
5. [Using the Bot](#using-the-bot)
    - [Getting Started](#getting-started)
    - [Slash Commands Guide](#slash-commands-guide)
6. [Advanced Features](#advanced-features)
    - [Changing Models](#changing-models)
    - [Whitelist Management Commands](#whitelist-management-commands)
7. [Character Creation Guide](#character-creation-guide)
8. [Credit and Acknowledgements](#credit-and-acknowledgements)

---

## Introduction

Aktiva AI is a versatile self-hosted Discord bot designed to enable users to interact seamlessly with multiple AI personalities in a single environment. Whether you're roleplaying, gathering information, looking for backup to support your argument, or just having fun, Aktiva AI leverages the latest advancements in AI technology through integrations like Hugging Face's Florence-2 Visual AI, OpenRouter APIs, and custom Language Model integration. With features ranging from dynamic character swapping to advanced memory systems, Aktiva AI is your go-to solution for creating an engaging AI-powered Discord server.

---

## Features

### Seamless Character Swapping
Talk to multiple AI characters through one bot:
- Easily trigger AI characters by saying their name or responding to their messages.
- Use `/list` to pull up a list of available characters on the server.
- Default AI, **Aktiva-chan**, can guide you through bot usage.
- Hide messages from the AI's context by starting the message with `//`.
- Each character uses webhooks for unique avatars, ensuring a personalized experience.

### Channel-Based Memory
Aktiva AI remembers channel-specific memories and locations:
- Each channel and thread has its own dedicated memory for an immersive interaction experience.
- Slash commands can modify or clear memory and location segments dynamically.

### Thread Support
Enjoy private or group interactions powered by full Discord thread support. Every thread has isolated memory management, allowing users to have private conversations or roleplaying sessions.

### Image Recognition
Integrated with A Cultured Finetune Microsoft's Florence-2 AI [MiaoshouAI/Florence-2-base-PromptGen-v2.0](https://huggingface.co/MiaoshouAI/Florence-2-base-PromptGen-v2.0), Aktiva AI provides powerful multimodal capabilities:
- Detect objects and aesthetics in uploaded images.
- Support for optional AI like Llava for enhanced image-based vibe detection.

### Character Message Editing and Deletion
For seamless content control:
- Edit bot responses directly in Discord using context menu commands.
- Delete bot responses to maintain moderation standards.

### Customizable AI Characters
Add unlimited characters to suit your needs:
- Place character JSON files in the `characters/` folder.
- SillyTavern's character card and Pygmalion AI card formats are fully supported for input.

### PDF File Reading Support
Upload PDF documents for AI characters to read, analyze, and provide insights during interactions.

### Web Search Integration
Powered by **DuckDuckGo**:
- Allow your AI characters to perform live web searches.
- Get accurate, real-time information during conversations.
- Retrieve Images, Videos, and Get Newest Headlines.
- Add `^` at the beginning of your message to enable web search function and `(keyword)` for the thing you want the AI to retrieve.

### Whitelist Management
Control which AI characters can respond in specific channels:
- Assign whitelists to channels using slash commands.
- Customize character availability per channel/thread for tailored interactions.

### OpenRouter API Integration
Expand the bot’s capabilities through OpenRouter:
- Switch AI models via commands to experiment with different models.
- Compatible with third-party AI providers.

---

## Prerequisites

1. **Large Language Model (LLM)**
   - Recommended models:
     - [Stheno - Llama 8B Model](https://huggingface.co/Lewdiculous/L3-8B-Stheno-v3.1-GGUF-IQ-Imatrix)
     - [Nyanade - Llama 7B Model](https://huggingface.co/Lewdiculous/Nyanade_Stunna-Maid-7B-v0.2-GGUF-IQ-Imatrix)

2. **Backend - Koboldcpp**
   - Install the backend framework: [Koboldcpp](https://github.com/LostRuins/koboldcpp)

3. **Florence 2 Finetune for Vision Tasks**
   - Preloaded with MiaoshouAI’s Florence-2-base for object recognition, text detection, and image compositional analysis.

4. **Config File**
   - A `.env` file containing the necessary API keys for Discord and OpenRouter.

---

## Installation Guide

1. Clone the Aktiva AI repository:
    ```bash
    git clone https://github.com/Iteranya/AktivaAI.git
    cd AktivaAI
    ```

2. Create a `.env` file with the required API keys (refer to `example.env` in the repository).

3. Install Python dependencies:
    ```bash
    python3 -m pip install -r requirements.txt
    ```

4. Launch your LLM using Koboldcpp and load the desired model.

5. Run the bot:
    ```bash
    python bot.py
    ```

---

## Using the Bot

### Getting Started
After starting the bot:
- Use `/help` for a quick tutorial on features and usage.
- Add interesting characters or experiments by placing JSON files in the `characters/` folder.

### Slash Commands Guide
Leverage the available commands to manipulate or customize the bot:
- `/list`: View all available characters.
- `/set_instruction`: Modify instructions for a specific AI character.
- `/set_global`: Change global data for the channel/thread.
- `/set_instruction`: Change the instruction data for the channel/thread.
- `/set_whitelist`: Add characters to a channel’s whitelist.
- `/clear_whitelist`: Clear character restrictions in the channel.

---

## Advanced Features

### Changing Models
Aktiva AI supports swapping between models dynamically. Use `/set_text_eval_model` to change the underlying AI evaluation model and `/get_text_eval_model` to view the active model.

### Whitelist Management Commands
Control character availability across channels with the following:
- `/set_whitelist`: Specify characters allowed in a channel.
- `/get_whitelist`: List allowed characters in the current channel.
- `/clear_whitelist`: Remove all channel-specific character restrictions.

---

## Character Creation Guide

Creating a custom character for Aktiva AI is simple:
1. JSON-based Configuration:
   - Refer to the structure of `characters/default.json`
2. SillyTavern and Pygmalion Character Cards:
   - Drag and drop compatible json files into the `characters/` folder to enable them.
   - Maximum Compatibility with Pygmalion AI Character Hub

---

## Credits and Acknowledgements

Aktiva AI owes its existence to:
- The amazing beta testers at the Ambruk Academy Discord Server.
- The incredible open-source community for libraries like Koboldcpp, Microsoft's Florence AI, and Hugging Face.
- You, the user, for pushing the boundaries of AI-driven Discord bots.

Join the journey. Happy experimenting! ❤️
