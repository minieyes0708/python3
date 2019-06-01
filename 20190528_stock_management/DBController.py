# -*- coding=utf8 -*-
class DBController:
    def __init__(self):
        self.db = None
        self.cursor = None
        self.db_name = '20190528_stock_management'
        self.tbl_name = '`everyday_close_info`'

    def open(self):
        import pymysql
        self.db = pymysql.connect('localhost', 'root', 'shenfen520', self.db_name)
        self.cursor = self.db.cursor()

    def __enter__(self):
        self.open()
        return self

    def close(self):
        self.db.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def execute(self, cmd):
        self.cursor.execute(cmd)

    def commit(self):
        self.db.commit()

    def fetchone(self, cmd):
        self.cursor.execute(cmd)
        return self.cursor.fetchone()

    def fetchall(self, cmd):
        self.cursor.execute(cmd)
        return self.cursor.fetchall()

    def last_date(self):
        return self.fetchone('SELECT MAX(`date_info`) FROM ' + self.tbl_name)[0]
