import datetime

from menu import MSG


class Command:

    def __init__(self, db: object) -> None:

        self.db = db

        self.dict_commands = {
            '1': ['Вывести список всех задач', self.show_current_users_tasks],
            '2': ['Добавить новую задачу', self.add_new_task],
            '3': ['Обновить задачу', self.update_current_task],
            '4': ['Вернуть задачу на заданный день', self.return_task_by_current_datetime],
            '5': ['Отметить выполненную задачу', self.set_task_as_done],
            '6': ['Вывести статистику', self.get_statistic],
        }

    def run_command(self, command: str) -> None:
        """Running a current command"""

        self.dict_commands[command][1]()


    def get_all_commands(self):
        """Return all commands"""

        return self.dict_commands


    def show_current_users_tasks(self):
        """Returns a list of current tasks"""

        data = self.db.return_tasks_data_whic_is_not_done()

        for task in data:
            MSG(f'''
                ID: {task['id']}
                Название: {task['name']}
                Таска: {task['task']}
                Дата: {task['date']}
                Статус выполнения: {task['is_done']}
            ''')()

    def add_new_task(self):

        name = input('Название: ')
        task = input('Таска: ')
        date = input('Дата: ')

        if not self.__check_date(date, "%Y-%m-%d %H:%M:%S"):
            return

        self.db.add_new_task(name, task, date)

    def update_current_task(self):

        data = {}
        id = int(input('Введите ID задачи: '))

        if not self.__check_row_on_exists(id):
            return

        task = self.db.return_current_task_by_id(id)

        data['name'] = input('Название: ') or task['name']
        data['task'] = input('Таска: ') or task['task']
        data['date'] = input('Дата: ') or task['date']

        if not self.__check_date(data['date'], "%Y-%m-%d %H:%M:%S"):
            return

        self.db.refactor_current_task(id, **data)


    def return_task_by_current_datetime(self):
        """Return a task by input date"""

        date = input('Введите дату: ')

        if not self.__check_date(date, "%Y-%m-%d"):
            return
        
        tasks = self.db.return_task_by_date(date)
        print(tasks)

        for task in tasks:
            MSG(f'''
                ID: {task[0]}
                Название: {task[1]}
                Таска: {task[2]}
                Дата: {task[3]}
                Статус выполнения: {task[4]}
            ''')()


    def set_task_as_done(self):

        task_id = input('Введите ID таски: ')

        if not self.__check_row_on_exists(task_id):
            return
        
        self.db.set_task_as_done(task_id)
        print('<Done>')

    
    def get_statistic(self):

        data = self.db.get_some_stat()

        for task in data:
            MSG(f'''
                Название: {task[0]}
                Таска: {task[1]}
                Дата: {task[2]}
            ''')()



    def __check_row_on_exists(self, id: int) -> bool:
        """Check if row exists"""
        if not self.db.check_task(id)[0]:
            MSG(f'Записи с ID {id} не существует')()

            return False
        
        return True
    

    def __check_date(self, date: str, format: str) -> bool:
        """Check if date has valid format"""

        try:
            datetime.datetime.strptime(date, (format))
            return True
        
        except:
                MSG(
                    f'Записи даты в формате {date} не допустима\
                    Валидный формат <день-месяц-год>')()

        

