# -*- coding=utf8 -*-
class DBController:
    def __init__(self):
        self.db = None
        self.cursor = None

    def open(self):
        import pymysql
        self.db = pymysql.connect('localhost', 'root', 'shenfen520', '20190528_stock_management')
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
