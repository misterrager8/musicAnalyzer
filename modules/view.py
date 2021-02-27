import sys

import PyInquirer.prompts


class CmdLnInterface:
    def __init__(self):
        main_options = [{
            'type': 'list',
            'name': 'menu',
            'message': 'What do you want to do?',
            'choices': []
        }]
        while True:
            answer = PyInquirer.prompt(main_options)

            if answer[""] == "":
                pass
