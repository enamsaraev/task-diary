import sqlite3 as sq

from datetime import datetime, time

class DB:

    def __init__(self) -> None:
        self.make_connection()

    
    def make_connection(self):
        """Connect app with DB"""

        with sq.connect('task.db') as conn:
            cur = conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS task(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                task TEXT NOT NULL,
                date TIMESTAMP CURRENT_TIMESTAMP,
                is_done BOOLEAN DEFAULT FALSE
                )""")
    

    def check_task(self, id: int) -> bool:
        """Return bool if task exists"""

        with sq.connect('task.db', detect_types=sq.PARSE_DECLTYPES) as conn:

            return conn.execute(
                f'SELECT EXISTS(SELECT id FROM task WHERE id="{id}" LIMIT 1)'
            ).fetchone()


    def return_tasks_data(self):
        """"""

        with sq.connect('task.db', detect_types=sq.PARSE_DECLTYPES) as conn:
            conn.row_factory = sq.Row
            return conn.execute(
                """SELECT * FROM task"""
            )
        
    
    def return_current_task_by_id(self, id: int):
        """Return task by id"""

        with sq.connect('task.db', detect_types=sq.PARSE_DECLTYPES) as conn:
            conn.row_factory = sq.Row
            return conn.execute(
                f'SELECT name, task, date FROM task WHERE id={id}'
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