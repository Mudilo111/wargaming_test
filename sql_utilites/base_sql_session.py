import sqlite3


class BaseSQLSession:

    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.curr = self.conn.cursor()

    def execute_query(self, sql_query):
        """
        Method that executes sql query
        :param sql_query: string containing sql query
        :return: result of executing sql query
        """
        self.curr.execute(sql_query)
        self.conn.commit()
        return self.curr.fetchall()

    def execute_script(self, script):
        """
        Method that executes script
        :param script: string cantaining script
        :return: None
        """
        self.conn.executescript(script)

    def session_end(self):
        """
        Method that ends sql session
        :return: None
        """
        self.curr.close()
        self.conn.close()

    def create_temp_copy(self):
        """
        Method that creates temporary copy of current database
        :return: Instance of database session
        """
        db_copy = self.__class__(db_name=':memory:')
        script = ''.join(line for line in self.conn.iterdump())
        db_copy.execute_script(script)
        return db_copy
