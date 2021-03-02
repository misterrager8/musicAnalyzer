import PyInquirer.prompts

from modules.ctrla import DB
from modules.model import Album, Artist, Song


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
