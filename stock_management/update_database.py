# -*- coding=utf8 -*-
from StockExchangeUsingJsonWebController import StockExchangeUsingJsonWebController
from OverTheCounterWebController import OverTheCounterWebController
from DBController import DBController
from datetime import timedelta, date


db_last_date = date.today()
with DBController() as db:
    db_last_date = db.last_date()


with StockExchangeUsingJsonWebController() as web:
    with DBController() as db:
        cur_date = db_last_date + timedelta(1)
        last_date = date.today()
        while cur_date <= last_date:
            print('stock exchange processing date = ', str(cur_date))
            web.update_date(cur_date)
            print('All Record Count = ', len(web.records))
            for cmd in web.records.values():
                db.execute(cmd)
            db.commit()
            web.records.clear()
            cur_date = cur_date + timedelta(1)

with OverTheCounterWebController() as web:
    with DBController() as db:
        cur_date = db_last_date + timedelta(1)
        last_date = date.today()
        while cur_date <= last_date:
            print('over the counter processing date = ', str(cur_date))
            web.update_date(cur_date)
            print('All Record Count = ', len(web.records))
            for cmd in web.records.values():
                db.execute(cmd)
            db.commit()
            web.records.clear()
            cur_date = cur_date + timedelta(1)
