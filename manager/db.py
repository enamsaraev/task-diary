import sqlite3 as sq

from datetime import datetime, time

from sqlquery import (
    CREATE_TABLE_TASK,
    CREATE_TABLE_STAT,
)

class DB:

    def __init__(self) -> None:
        self.make_connection()

    
    def make_connection(self):
        """Connect app with DB"""

        with sq.connect('task.db') as conn:
            conn.execute(CREATE_TABLE_TASK)
            conn.execute(CREATE_TABLE_STAT)
    

    def check_task(self, id: int) -> bool:
        """Return bool if task exists"""

        with sq.connect('task.db', detect_types=sq.PARSE_DECLTYPES) as conn:
            return conn.execute(
                f'SELECT EXISTS(SELECT id FROM task WHERE id="{id}" LIMIT 1)'
            ).fetchone()


    def return_tasks_data_whic_is_not_done(self):
        """"""

        with sq.connect('task.db', detect_types=sq.PARSE_DECLTYPES) as conn:
            conn.row_factory = sq.Row
            return conn.execute(
                """SELECT * FROM task WHERE is_done=False"""
            )
        
    
    def return_current_task_by_id(self, id: int):
        """Return task by id"""

        with sq.connect('task.db', detect_types=sq.PARSE_DECLTYPES) as conn:
            conn.row_factory = sq.Row
            return conn.execute(
                f'SELECT name, task, date, is_done FROM task WHERE id={id}'
            ).fetchone()
        

    def add_new_task(self, name: str, task: str, date: str):
        """Adding a new tasj to the db"""

        with sq.connect('task.db', detect_types=sq.PARSE_DECLTYPES) as conn:
            conn.execute(
                f'INSERT INTO task (name, task, date) \
                VALUES ("{name}", "{task}", "{date}")'
            )


    def refactor_current_task(self, id: int, name: str, task: str , date: str):
        """Updating current task"""

        with sq.connect('task.db', detect_types=sq.PARSE_DECLTYPES) as conn:
            conn.execute(
                f'UPDATE task SET name="{name}", task="{task}", date="{date}" WHERE id={id}'
            )

    
    def return_task_by_date(self, dt: str):
        """Return a list of all tasks by current input date"""

        dt = datetime.combine(datetime.strptime(dt, '%Y-%m-%d'), time())
        dt_end = datetime.combine(dt, time(23, 59, 59))

        with sq.connect('task.db', detect_types=sq.PARSE_DECLTYPES) as conn:
            return conn.execute(
                """SELECT * FROM task WHERE date BETWEEN ? AND ?""", (dt, dt_end)
            ).fetchall()
        

    def set_task_as_done(self, id: int):
        """"""

        dt = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

        with sq.connect('task.db', detect_types=sq.PARSE_DECLTYPES) as conn:
            conn.execute(
                f'UPDATE task SET is_done=True WHERE id={id}'
            )
            conn.execute(
                f'INSERT INTO stat (date, task_id) \
                VALUES ("{dt}", "{id}")'
            )

    
    def get_some_stat(self):
        """"""

        with sq.connect('task.db', detect_types=sq.PARSE_DECLTYPES) as conn:
            return conn.execute(
                f'SELECT task.name, task.task, stat.date from stat \
                  INNER JOIN task ON task.id = stat.task_id'
            ).fetchall()