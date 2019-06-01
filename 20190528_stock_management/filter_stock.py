import time
from functools import partial
from datetime import date, timedelta
from DBController import DBController

def rise_2_percent(stock_info, days):
    if len(stock_info) < days:
        return False

    rise_fall = []
    for day in range(days):
        rise_fall.append(float(stock_info[-1 * (day + 1)]['rise_fall'].replace('X','')))

    if all(map(lambda x: x > 2, rise_fall)):
        return True
    else:
        return False

filters = (
    partial(rise_2_percent, days = 2),
)

passed_stocks = []
start_time = time.clock()
with DBController() as db:
    stock_ids = db.get_stock_id_list()
    total_stock_count = len(stock_ids)
    for stock_index in range(total_stock_count):
        print('{0} / {1}'.format(stock_index, total_stock_count))
        stock_id = stock_ids[stock_index]
        stock_info = db.get_stock_info_by_id(stock_id, date.today() - timedelta(30), date.today())
        success = True
        for filter in filters:
            if filter(stock_info) == False:
                success = False
                break
        if success:
            passed_stocks.append(stock_id)

for stock in passed_stocks:
    print(stock)
print('total passed stock count = ', len(passed_stocks))
