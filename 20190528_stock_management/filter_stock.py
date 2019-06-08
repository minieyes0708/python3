import time
from functools import partial
from datetime import date, timedelta
from DBController import DBController


def rise_percent(stock_info, percent, days):
    if len(stock_info) < days: return False

    rise_fall = [stock_info[-(day + 1)]['rise_fall'].replace('X','') for day in range(days)]
    open_price = [stock_info[-(day + 1)]['open_price'].replace(',','') for day in range(days)]

    rise_fall_percentage = [float(rf) * 100 / float(op) for (rf, op) in zip(rise_fall, open_price)]
    if all(map(lambda x: x > percent, rise_fall_percentage)):
        return True
    else:
        return False


def deal_count_max(stock_info, now_days, past_days):
    max_deal_count = max([info['deal_stock_count'] for info in stock_info[-past_days:] if info['rise_fall'][0] != '-'])
    if max_deal_count in [info['deal_stock_count'] for info in stock_info[-now_days:] if info['rise_fall'][0] != '-']:
        return True
    else:
        return False


def highest_price_max(stock_info, now_days, past_days):
    max_highest_price = max([info['highest_price'] for info in stock_info[-past_days:]])
    if max_highest_price in [info['highest_price'] for info in stock_info[-now_days:]]:
        return True
    else:
        return False


filters = (
    partial(rise_percent, percent = 1, days = 2),
    partial(deal_count_max, now_days = 3, past_days = 30),
    partial(highest_price_max, now_days = 3, past_days = 30),
)

passed_stocks = []
start_time = time.clock()
with DBController() as db:
    stock_ids = db.get_stock_id_list()
    total_stock_count = len(stock_ids)
    for stock_index in range(total_stock_count):
        print('{0} / {1}'.format(stock_index, total_stock_count))
        stock_id = stock_ids[stock_index]
        stock_info = db.get_stock_info_by_id(stock_id, date.today() - timedelta(60), date.today())
        success = True
        for filter in filters:
            if not filter(stock_info):
                success = False
                break
        if success:
            passed_stocks.append(stock_id)

for stock in passed_stocks:
    print(stock)
print('total passed stock count = ', len(passed_stocks))
print('total time took = {0}s'.format(time.clock() - start_time))
