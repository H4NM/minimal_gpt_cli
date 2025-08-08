#! /usr/bin/env python3

import requests
import sys
import os
import re
from datetime import datetime

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
    CLEAR = "\033c"

USER_NAME='You'
CHATGPT_NAME='CliGPT'
CHAT_HISTORY_PATH=r'/Users/hami/Documents/cligpt-results/'
WELCOME_MSG=f"""Welcome!
Ask me anything. Special commands:
  - {Colors.BOLD}quit, exit, goodbye,{Colors.END} and {Colors.BOLD}bye;{Colors.END} terminate application
  - {Colors.BOLD}clear{Colors.END}; clears the terminal screen
  - {Colors.BOLD}save{Colors.END}; saves the entire chat history to one file
  - {Colors.BOLD}save code{Colors.END}; saves all of the code provided by {CHATGPT_NAME}
"""

LANGUAGES = {
        'python' : {
		'suffix': 'py'
	},
        'bash' : {
		'suffix': 'sh'
	},
        'powershell' : {
		'suffix': 'ps'
	},
        'javascript' : {
		'suffix': 'js'
	},
        'csharp' : {
		'suffix': 'cs'
	},
        'go' : {
		'suffix': 'go'
	},
        'ruby' : {
		'suffix': 'rb'
	},
        'unidentified': {
		'suffix': 'txt'
        }
}

REGEX_PATTERNS={
        'codeblock': r'^[\s\t]{0,}```',
        'code_language': '|'.join([ language for language in LANGUAGES if not language == 'unidentified'])
}

OS=""

CODE_HISTORY = []

END_MSGS = ['quit','exit','bye','goodbye']

def replace_code_tags(match):
    if replace_code_tags.counter % 2 == 0:
        replace_code_tags.counter = 1
        return Colors.YELLOW
    else:
        replace_code_tags.counter = 0
        return Colors.END

replace_code_tags.counter = 0

def enable_ansi():
    global OS
    if os.name == 'nt':
        #To make ansi escape sequences work for windows
        os.system("")
        OS='windows'
    else:
        OS='unix'

def print_goodbye():
    print(f'{Colors.BOLD}Goodbye!{Colors.END}')

def get_input():
    try:
        while True:
                msg = input(f'{Colors.GREEN}{USER_NAME}:{Colors.END} ')
                stripped_msg = msg.strip()
                if stripped_msg in END_MSGS:
                        raise Exception('Self quit')
                elif stripped_msg == 'clear':
                        print(Colors.CLEAR, end="")
                elif stripped_msg == 'save':
                        if len(BODY['messages']) > 0:
                                parsed_message_history = []

                                for old_message in BODY['messages']:
                                        if old_message['role'] == 'user':
                                                writer = USER_NAME
                                        else:
                                                writer = CHATGPT_NAME
                                        parsed_message_history.append(writer+': '+old_message['content'])

                                file_path = save_codeblock("\n".join(parsed_message_history), 'unidentified')
                                print(f'[+] Saved the chat history to {file_path}')
                elif stripped_msg == 'save code':
                        if len(CODE_HISTORY) > 0:
                                file_path = save_codeblock("\n".join(CODE_HISTORY), 'unidentified')
                                print(f'[+] Saved the code history to {file_path}')
                        else:
                                print(f'[!] No code history to save')
                elif len(stripped_msg) > 0:
                        return msg
    except:
        print_goodbye()
        exit(1)

def show_output(response, status):

    if status == 'success' and response.status_code == 200:
        response_json = response.json()
        cgpt_msg = response_json['choices'][0]['message']['content']
        cgpt_role = response_json['choices'][0]['message']['role']
        BODY['messages'].append({'role': cgpt_role, 'content': cgpt_msg})
        codeblock = re.search(REGEX_PATTERNS['codeblock'], cgpt_msg, flags=re.DOTALL|re.M)

        code = []
        if codeblock:
                global CODE_HISTORY
                codeblock_lang_found = re.search(REGEX_PATTERNS['codeblock']+'('+REGEX_PATTERNS['code_language']+')', cgpt_msg, flags=re.DOTALL|re.M)
                if codeblock_lang_found:
                        code_language = codeblock_lang_found.group(1)
                else:
                        code_language = "unidentified"
                code = re.findall(REGEX_PATTERNS['codeblock']+'(.*?)'+REGEX_PATTERNS['codeblock']+'$',
                cgpt_msg,
                flags=re.M|re.DOTALL)
                codeblocks = len(code)
                CODE_HISTORY += code
                cgpt_msg = re.sub(r'```', replace_code_tags, cgpt_msg)

        print(f'{Colors.RED}{CHATGPT_NAME}:{Colors.END}',cgpt_msg)

        if code:
                if codeblocks == 1:
                        print(f'= Found a codeblock. Do you want to save it to file [y/N]?')
                else:
                        print(f'= Found {codeblocks} codeblocks. Do you want to save them to files [y/N]?')
                fs_choice = input(f'{Colors.BLINK}~{Colors.END}: ').strip()
                if len(fs_choice) == 0 or re.search('^[nN]$', fs_choice):
                        pass
                elif re.search('^[yY]$', fs_choice):

                        if codeblocks > 1:
                                print('= One whole file or separate files per codeblock? [sep/One]')
                                fs_choice = input(f'{Colors.BLINK}~{Colors.END}: ').strip()

                                if re.search('^sep', fs_choice, flags=re.I):
                                        for counter, codesnippet in enumerate(code):
                                                file_path = save_codeblock(codesnippet, code_language, counter)
                                                print(f'[+] Saved file to {file_path}')
                                else:
                                        file_path = save_codeblock("\n".join(code), code_language)
                                        print(f'[+] Saved file to {file_path}')
                        else:
                                file_path = save_codeblock(codesnippet, code_language)
                                print(f'[+] Saved file to {file_path}')


    elif status == 'fail':
        print(f'{Colors.RED}ERROR: Unable to reach url {URL}. {Colors.END}')
    else:
        print(f'{Colors.RED}ERROR: {response.text}{Colors.END}')

def save_codeblock(codeblock, language, increment=1):
        if CHAT_HISTORY_PATH:
                path=CHAT_HISTORY_PATH
        else:
                if OS == 'windows':
                        path=r'C:\\Windows\\Temp\\'
                else:
                        path=r'/tmp/'

        ts = datetime.now().strftime('%Y%m%d-%H-%M-%S')

        file_path=f'{path}cligpt-{ts}-{increment}.{LANGUAGES[language]["suffix"]}'

        with open(file_path, 'wt') as code_file:
                code_file.write(codeblock)
                code_file.close()
        return file_path



if __name__ == '__main__':
    enable_ansi()
    print(f'{Colors.RED}{CHATGPT_NAME}:{Colors.END}',WELCOME_MSG)
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
    else:
        message = get_input()

    BODY['messages'].append({'role': 'user', 'content': message})

    while True:
        try:
                resp = requests.post(url=URL, headers=HEADER, json=BODY)
                status = 'success'
        except:
                resp = None
                status = 'fail'
        show_output(resp, status)
        message = get_input()

        BODY['messages'].append({'role': 'user', 'content': message})
