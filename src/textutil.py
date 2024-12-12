import re



def clean_text(text:str):
    """
    Remove emojis, trailing whitespace, line breaks, and bracket-like characters from a given string.
    
    Args:
        text (str): Input string that may contain emojis, whitespace, line breaks, and trailing characters
    
    Returns:
        str: Cleaned string 
    """
    # Emoji pattern
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        "]+", flags=re.UNICODE)
    
    # Remove trailing whitespace and line breaks first
    text = text.rstrip()
    
    # Remove emojis
    text_without_emoji = emoji_pattern.sub(r'', text)
    
    # Remove trailing bracket-like characters, with more inclusive matching
    cleaned_text = re.sub(r'[)\]>:;,\s]+$', '', text_without_emoji)
    
    return cleaned_text.rstrip()

def remove_last_word_before_final_colon(text: str) -> str:
    # Define the regex pattern to find the last word before the final colon
    pattern = r'\b\w+\s*:$'
    
    # Use re.sub to replace the matched pattern with an empty string
    result = re.sub(pattern, '', text)
    
    return result.strip()  # Remove any leading or trailing whitespace

def remove_string_before_final(data: str) -> str:
    substrings = ["[/","[System", "[SYSTEM", "[Reply", "[REPLY", "(System", "(SYSTEM","[End]","[End"]
    
    for substr in substrings:
        if data.endswith(substr):
            return data[:-len(substr)]
    
    return data

def remove_fluff(text: str) -> str:
    # Find the last pair of asterisks and the content between them
    pattern = r'\*(.*?)\*'
    
    # Use re.findall to get all matches and re.sub to remove the last one
    matches = re.findall(pattern, text)
    if matches:
        # Get the last match and construct the regex to remove it
        last_fluff = re.escape(f"*{matches[-1]}*")
        text = re.sub(last_fluff, '', text, count=1)
    
    return text.strip()  # Remove any extra whitespace
