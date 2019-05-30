# -*- coding=utf8 -*-
class DBController:
    def __init__(self):
        self.db = None

    def open(self):
        import pymysql
        self.db = pymysql.connect('localhost', 'root', 'shenfen520', '20190528_stock_management')

    def __enter__(self):
        self.open()
        return self

    def close(self):
        self.db.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def execute(self, cmd):
        cursor = self.db.cursor()
        cursor.execute(cmd)
        cursor.close()
