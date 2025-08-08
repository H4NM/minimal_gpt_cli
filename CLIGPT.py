#! /usr/bin/env python3

import requests
import sys
import os
import re
from datetime import datetime

### APIs
import APIs.OpenAI
import APIs.AwanLLM
import settings

USED_GPT = APIs.AwanLLM.AwanLLM
CODE_HISTORY = []

def replace_code_tags(match):
    if replace_code_tags.counter % 2 == 0:
        replace_code_tags.counter = 1
        return Colors.YELLOW
    else:
        replace_code_tags.counter = 0
        return Colors.END

replace_code_tags.counter = 0

def ensure_ansi_interpretation():
    if os.name == 'nt':
        #To make ansi escape sequences work for windows
        os.system("")

def print_welcome_message():
        print(f'{settings.Colors.RED}{settings.CLIGPT_NAME}:{settings.Colors.END}',settings.WELCOME_MSG)


def print_goodbye():
    print(f'{settings.Colors.BOLD}Goodbye!{settings.Colors.END}')

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

def show_output(cgpt_msg, status):

    if status == 'success':
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
        print(f'{settings.Colors.RED}ERROR: Unable to reach GPT URL. {settings.Colors.END}')
    else:
        print(f'{settings.Colors.RED}ERROR: {response.text}{settings.Colors.END}')

def save_codeblock(codeblock, language, increment=1):
        ts = datetime.now().strftime('%Y%m%d-%H-%M-%S')
        file_path=f'{settings.CHAT_HISTORY_PATH}cligpt-{ts}-{increment}.{LANGUAGES[language]["suffix"]}'
        with open(file_path, 'wt') as code_file:
                code_file.write(codeblock)
                code_file.close()
        return file_path

def parse_gpt_response(response:str = "", used_gpt:str = ""):
        cgpt_msg = response_json['choices'][0]['message']['content']
        cgpt_role = response_json['choices'][0]['message']['role']


if __name__ == '__main__':
    ensure_ansi_interpretation()
    print_welcome_message()
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
    else:
        message = get_input()

    gpt = USED_GPT()

    while True:
        message = get_input()
        BODY['messages'].append({'role': 'user', 'content': message})

        try:
                resp = requests.post(url=gpt.URL, headers=gpt.HEADERS, json=gpt.BODY)
                status = 'success'
        except:
                resp = None
                status = 'fail'
        
        gpt_role, gpt_msg = parse_gpt_response(response=resp,used_gpt=gpt.NAME)
        BODY['messages'].append({'role': gpt_role, 'content': gpt_msg})
        show_output(gpt_msg, status)
