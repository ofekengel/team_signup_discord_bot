import sqlite3
from typing import List


class DBCommunicator:
    def __init__(self, db_path: str):
        self.__conn = sqlite3.connect(db_path)
        self.cur = self.__conn.cursor()

    def execute_query(self, query: str):
        try:
            self.cur.execute(query)
            self.__conn.commit()
        except Exception as e:
            self.exit()
            raise e

    def get_result(self) -> List:
        return self.cur.fetchall()

    def exit(self):
        self.__conn.close()
