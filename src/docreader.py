import PyPDF2
import config
import aiohttp
import google.generativeai as genai


class DocReader:
    def __init__(self, path):
        self.path = path
        self.text = self.pdf_to_text(path)
    
    def pdf_to_text(self, pdf_path):
        """
        Extracts text from a PDF file.
        Args:
            pdf_path: The path to the PDF file.
        Returns:
            The extracted text as a string, or None if an error occurs.
        """
        try:
            with open(pdf_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                num_pages = len(pdf_reader.pages)
                text = ""
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()
           
            return text
        except FileNotFoundError:
            print(f"Error: PDF file not found at {pdf_path}")
            return None
        except PyPDF2.errors.PdfReadError:
            print(f"Error: Could not read PDF. The file might be corrupted or encrypted.")
            return None
        except Exception as e:  # Catch other potential errors
            print(f"An unexpected error occurred: {e}")
            return None
    
    async def llm_eval(self):
        if not self.text:
            print("No text to evaluate")
            return None
        gemini_eval = await self.gemini_eval()
        if gemini_eval==None:
            return await self.router_eval()
        else:
            return gemini_eval

    async def gemini_eval(self):
        genai.configure(api_key=config.gemini_token)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = await model.generate_content_async(f"[{self.text}] \n=====\n Write a summary followed with a detailed analysis of the text above in Markdown Format")

        return response.text

    async def router_eval(self, 
                       include_image_url=None):

        
        model = config.text_evaluator_model
        final_prompt = f"[{self.text}] \n=====\n Write a summary followed with a detailed analysis of the text above in Markdown Format"
        
        # Prepare messages payload
        messages = [{
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": final_prompt
                }
            ]
        }]
        
        # Add image if provided
        if include_image_url:
            messages[0]["content"].append({
                "type": "image_url",
                "image_url": {
                    "url": include_image_url
                }
            })
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {config.openrouter_token}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model,
                        "messages": messages
                    }
                ) as response:
                    # Raise exception for bad HTTP status
                    response.raise_for_status()
                    result = await response.json()
                    print(str(result))
                    if result.get('choices',None)!=None:
                        return result['choices'][0]['message']['content']
                    else:
                        return f"Error Reading File: {result['error']['message']}, Notify User That An Error Occured."
        except aiohttp.ClientError as e:
            print(f"Network error in LLM evaluation: {e}")
        except (KeyError, ValueError) as e:
            print(f"Parsing error in LLM response: {e}")
        except Exception as e:
            print(f"Unexpected error in LLM evaluation: {e}")
        
        return None
