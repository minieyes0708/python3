# -*- coding=utf8 -*-
def filter_stock():
    from functools import partial
    from Profiler import Profiler
    from datetime import date, timedelta
    from DBController import DBController

    def rise_percent(all_stock_info, start_index, end_index, percent, days):
        if end_index - start_index < days: return False

        rise_fall = [all_stock_info[end_index - (day + 1)]['rise_fall'] for day in range(days)]
        open_price = [all_stock_info[end_index - (day + 1)]['open_price'] for day in range(days)]

        rise_fall_percentage = [float(rf) * 100 / float(op) for (rf, op) in zip(rise_fall, open_price)]
        if all(map(lambda x: x > percent, rise_fall_percentage)):
            return True
        else:
            return False

    def deal_count_max(all_stock_info, start_index, end_index, now_days, past_days):
        if end_index - start_index < past_days: return False

        max_deal_count = max([info['deal_stock_count'] for info in all_stock_info[end_index - past_days : end_index]])
        if max_deal_count in [info['deal_stock_count'] for info in all_stock_info[end_index - now_days : end_index]]:
            return True
        else:
            return False

    def highest_price_max(all_stock_info, start_index, end_index, now_days, past_days):
        if end_index - start_index < past_days: return False

        max_highest_price = max([info['highest_price'] for info in all_stock_info[end_index - past_days : end_index]])
        if max_highest_price in [info['highest_price'] for info in all_stock_info[end_index - now_days : end_index]]:
            return True
        else:
            return False

    filters = (
        partial(rise_percent, percent = 1, days = 2),
        partial(deal_count_max, now_days = 3, past_days = 30),
        partial(highest_price_max, now_days = 3, past_days = 30),
    )

    passed_stocks = []
    profiler = Profiler()
    with DBController() as db:
        all_stock_info = db.fetch_all_stocks_in_time(date.today() - timedelta(60), date.today())

        def loop_all_stocks():
            end_index = 0
            while end_index != len(all_stock_info):
                start_index = end_index
                cur_stock_id = all_stock_info[start_index]['stock_id']
                while end_index != len(all_stock_info) and cur_stock_id == all_stock_info[end_index]['stock_id']:
                    end_index += 1
                yield (start_index, end_index)

        for (start_index, end_index) in loop_all_stocks():
            profiler.start()
            print('{0} - {1} / {2}'.format(start_index, end_index, len(all_stock_info)))
            success = True
            for filter in filters:
                if not filter(all_stock_info, start_index, end_index):
                    success = False
                    break
            if success:
                passed_stocks.append(all_stock_info[start_index]['stock_id'])
            profiler.stamp(end_index - start_index)
            print('remaining time = {0}:{1}:{2}'.format(*profiler.remaining_time(len(all_stock_info) - end_index)))

    return passed_stocks


if __name__ == '__main__':
    passed_stocks = filter_stock()
    for stock in passed_stocks:
        print(stock)
    print('total passed stock count = ', len(passed_stocks))
