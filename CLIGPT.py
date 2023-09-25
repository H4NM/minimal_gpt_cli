import requests
import sys
import json


API_KEY='YOUR API KEY'
URL='https://api.openai.com/v1/chat/completions'
HEADER= {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {API_KEY}'
}
BODY={
            'model': 'gpt-3.5-turbo',
            'messages': [],
            'temperature': 0.7,
            'max_tokens': 100
        }

class Colors:
    """ ANSI color codes """
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    YELLOW = "\033[1;33m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"

def enable_ansi():
    import os
    if os.name == 'nt':
        #To make ansi escape sequences work for windows
        os.system("")
    del os

def get_input():
    try:
        msg = input(f'{Colors.BOLD}You:{Colors.END} ')
        if not msg:
            return get_input()
        return msg
    except:
        print(f'{Colors.BOLD}Goodbye!{Colors.END}')
        exit(1)

def show_output(response):
    if response.status_code == 200:
        json_resp = response.json()
        cgpt_msg = json_resp['choices'][0]['message']['content']
        cgpt_role = json_resp['choices'][0]['message']['role']
        BODY['messages'].append({'role': cgpt_role, 'content': cgpt_msg})

        if '```' in cgpt_msg:
            
        print(f'{Colors.BOLD}ChatGPT:{Colors.END}', cgpt_msg)
    else:
        print(f'ERROR: {response.text}')

if __name__ == '__main__':
    enable_ansi()
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
    else:
        message = get_input()

    BODY['messages'].append({'role': 'user', 'content': message})
    
    while True:
        
        resp = requests.post(url=URL, headers=HEADER, json=BODY)
        show_output(resp)
        message = get_input()
        BODY['messages'].append({'role': 'user', 'content': message})
