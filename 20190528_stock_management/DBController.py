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
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

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
        from datetime import date, timedelta
        return self.fetchone('SELECT MAX(`date_info`) FROM ' + self.tbl_name)['MAX(`date_info`)'] or date.today() - timedelta(30 * 3)

    def first_date(self):
        return self.fetchone('SELECT MIN(`date_info`) FROM ' + self.tbl_name)['MIN(`date_info`)']

    def get_stock_id_list(self):
        cmd = 'SELECT `stock_id` FROM ' + self.tbl_name + ' GROUP BY `stock_id`'
        return [id['stock_id'] for id in self.fetchall(cmd)]

    def fetch_all_stocks_in_time(self, start_date = None, end_date = None):
        from datetime import date
        if not start_date:
            start_date = self.first_date()
        if not end_date:
            end_date = date.today()
        return self.fetchall('''
        SELECT `date_info`, `stock_id`, `stock_name`, `deal_stock_count`, `open_price`, `highest_price`, `lowest_price`, `close_price`, `rise_fall` FROM {tbl_name}
        WHERE `date_info` >= "{start_date}" AND `date_info` <= "{end_date}"
        ORDER BY `stock_id`, `date_info`
        '''.format(**{
            'tbl_name': self.tbl_name,
            'start_date': start_date,
            'end_date': end_date,
        }))

    def get_stock_info_by_id(self, stock_id, start_date = None, end_date = None):
        from datetime import date
        if not start_date:
            start_date = self.first_date()
        if not end_date:
            end_date = date.today()
        return self.fetchall('''
        SELECT `date_info`, `stock_name`, `deal_stock_count`, `open_price`, `highest_price`, `lowest_price`, `close_price`, `rise_fall` FROM {tbl_name}
        WHERE `stock_id` = "{stock_id}" AND `date_info` >= "{start_date}" AND `date_info` <= "{end_date}"
        ORDER BY `date_info`
        '''.format(**{
            'tbl_name': self.tbl_name,
            'stock_id': stock_id,
            'start_date': start_date,
            'end_date': end_date,
        }))
