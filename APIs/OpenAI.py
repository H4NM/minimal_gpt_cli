API_KEY=''
URL='https://api.openai.com/v1/chat/completions'
HEADER= {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {API_KEY}'
}
BODY={
            #'model': 'gpt-3.5-turbo',
            'model': 'gpt-4',
            'messages': [],
            'temperature': 0.7,
            'max_tokens': 1000
        }
