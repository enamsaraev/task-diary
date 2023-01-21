from textwrap import dedent
from dataclasses import dataclass

class Menu:

    def __init__(self, command: object) -> None:
        
        self.command = command


    def run(self) -> None:
        """Running menu"""

        self.show_menu()
        self.call_command()


    def show_menu(self) -> None:
        """Print menu commands in terminal"""

        for key, command in self.command.get_all_commands().items():
            print(f'<{key}> {command[0]}')

    
    def recieve_menu_command(self):
        """Get user menu command input"""

        user_msg = input('<Введите номер задачи> ')

        return user_msg
    

    def call_command(self):

        command = self.recieve_menu_command()
        self.command.run_command(command)


@dataclass
class MSG:
    msg: str

    def __call__(self) -> bool:

        print(dedent(f'''
                    ------------------
                    {self.msg}
                    ------------------
                    '''
            ))