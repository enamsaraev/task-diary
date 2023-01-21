from menu import Menu
from command import Command
from db import DB

db = DB()
command = Command(db)
menu = Menu(command)


if __name__ == '__main__':

    while True:
        menu.run()
