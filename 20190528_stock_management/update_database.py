# -*- coding=utf8 -*-
import time
from StockExchangeWebController import StockExchangeWebController
from DBController import DBController
from datetime import timedelta, date


with StockExchangeWebController() as web:
    with DBController() as db:
        cur_date = db.last_date() + timedelta(1)
        last_date = date.today()
        while cur_date <= last_date:
            start_time = time.clock()
            print('processing date = ', str(cur_date))
            web.select_date(cur_date)
            web.update_all_types()
            print('All Record Count = ', len(web.records))
            for cmd in web.records:
                db.execute(cmd)
            db.commit()
            web.records.clear()
            cur_date = cur_date + timedelta(1)
            print('total time took {0:.2f}s'.format(time.clock() - start_time))
