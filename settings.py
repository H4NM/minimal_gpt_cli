

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

