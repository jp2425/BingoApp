import sqlite3

from ConfigSIngleton import ConfigSingleton
from repo.RepoAbsClass import RepoAbsClass


class SQLiteRepo(RepoAbsClass):
    """
    Class used to interact with the database
    """

    def __init__(self):

        #initialization of the database
        self._conn = sqlite3.connect('numbers.db', check_same_thread=False)
        self._cursor = self._conn.cursor()
        self._cursor.execute(
            'CREATE TABLE IF NOT EXISTS numbers (id INTEGER PRIMARY KEY AUTOINCREMENT, number INTEGER UNIQUE)')
        self._conn.commit()

    def insert_number_action(self, number: int):
        """
        Function to insert a number into the database.
        :param number: Number to insert in the database
        """

        self._cursor.execute("INSERT INTO numbers (number) VALUES (?)", (number,))
        self._conn.commit()

    def delete_number_action(self, number:int):
        """
        Function to delete a number into the database.
        :param number: Number to delete in the database
        """

        self._cursor.execute("DELETE FROM numbers WHERE number = (?)", (number,))
        self._conn.commit()

    def get_all_numbers(self):
        """
        Function used to get all numbers in the database.
        """
        return self._conn.execute("SELECT number FROM numbers").fetchall()

    def get_last(self):
        """
        Function to get the last number inserted in the database
        """


        self._cursor.execute("SELECT number FROM numbers ORDER BY id DESC LIMIT 1")
        try:
            return self._cursor.fetchone()[0]
        except:
            return str(ConfigSingleton().get_page_config("last")["default_last_message_empty_values"]) #no value in database
