import os

class ChatGPT:
    GPT_NAME="ChatGPT"
    API_KEY= os.environ['CHATGPT_API_KEY'] if 'CHATGPT_API_KEY' in os.environ else ""
    URL='https://api.openai.com/v1/chat/completions'
    MODEL_NAME='gpt-4'

    HEADERS= {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    BODY={
                'model': MODEL_NAME,
                'messages': [],
                'temperature': 0.7,
                'max_tokens': 1000
    }
