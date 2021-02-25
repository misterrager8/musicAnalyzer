import sys

import PyInquirer.prompts


class CmdLnInterface:
    def __init__(self):
        main_options = [{
            'type': 'list',
            'name': 'menu',
            'message': 'What do you want to do?',
            'choices': [
                "CREATE",
                "READ",
                "UPDATE",
                "DELETE",
                "EXIT"
            ]
        }]
        while True:
            answer = PyInquirer.prompt(main_options)

            if answer["menu"] == "CREATE":
                self.create()
            elif answer["menu"] == "READ":
                self.read()
            elif answer["menu"] == "UPDATE":
                self.update()
            elif answer["menu"] == "DELETE":
                self.delete()
            elif answer["menu"] == "EXIT":
                sys.exit()

    def create(self):
        print("create")

    def read(self):
        print("read")

    def update(self):
        print("update")

    def delete(self):
        print("delete")
