url = "https://api.awanllm.com/v1/chat/completions"
api_key = "9c83ac55-26db-4691-8e9c-0f1964a3dc78"
model_name = "Meta-Llama-3.1-70B-Instruct"

payload = {
  "model": f"{model_name}",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"},
    {"role": "assistant", "content": "Hi!, how can I help you today?"}
  ],
  "repetition_penalty": 1.1,
  "temperature": 0.7,
  "top_p": 0.9,
  "top_k": 40,
  "max_tokens": 1024,
  "stream": True
}

headers = {
  'Content-Type': 'application/json',
  f'Authorization': f"Bearer {api_key}"
}
