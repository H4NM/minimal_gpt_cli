import os

class VeniceAI:
  GPT_NAME="VeniceAI"
  API_KEY= os.environ['VENICEAI_API_KEY'] if 'VENICEAI_API_KEY' in os.environ else ""
  URL="https://api.venice.ai/api/v1/chat/completions"
  MODEL_NAME = "venice-uncensored"
  INITIAL_LLM_INSTRUCTIONS="You are a helpful assistant."

  HEADERS = {
    'Content-Type': 'application/json',
    f'Authorization': f"Bearer {API_KEY}"
  }
  BODY = {
    "model": f"{MODEL_NAME}",
    "messages": [
      {"role": "system", "content": INITIAL_LLM_INSTRUCTIONS}
    ],
    "repetition_penalty": 1.1,
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40,
    "max_tokens": 1024,
    "stream": True
  }

