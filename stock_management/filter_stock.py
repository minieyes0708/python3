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

        max_deal_count = max([int(info['deal_stock_count']) for info in all_stock_info[end_index - past_days : end_index]])
        if max_deal_count in [int(info['deal_stock_count']) for info in all_stock_info[end_index - now_days : end_index]]:
            return True
        else:
            return False

    def highest_price_max(all_stock_info, start_index, end_index, now_days, past_days):
        if end_index - start_index < past_days: return False

        max_highest_price = max([float(info['highest_price'].replace(',','')) for info in all_stock_info[end_index - past_days : end_index]])
        if max_highest_price in [float(info['highest_price'].replace(',','')) for info in all_stock_info[end_index - now_days : end_index]]:
            return True
        else:
            return False


    def continue_rising(all_stock_info, start_index, end_index, inspect_days, diff_days, rising_percentage):
        if end_index - start_index < max(inspect_days): return False

        success = True
        for day in inspect_days:
            previous_price = float(all_stock_info[end_index - day - diff_days - 1]['close_price'].replace(',',''))
            current_price = float(all_stock_info[end_index - day - 1]['close_price'].replace(',',''))
            if previous_price * rising_percentage > current_price:
                success = False
                break
        return success


    def close_price_in_range(all_stock_info, start_index, end_index, minval, maxval):
        import sys
        if not minval: minval = sys.minfloat
        if not maxval: maxval = sys.maxfloat
        if float(all_stock_info[end_index - 1]['close_price']) < minval: return False
        if float(all_stock_info[end_index - 1]['close_price']) > maxval: return False
        return True


    filters = (
      (
          partial(continue_rising, inspect_days = [0,10,20,30], diff_days = 10, rising_percentage = 1.02),
          partial(close_price_in_range, minval = 10, maxval = 150),
      ),
      (
          partial(rise_percent, percent = 1, days = 2),
          partial(deal_count_max, now_days = 3, past_days = 30),
          partial(highest_price_max, now_days = 3, past_days = 30),
      ),
    )

    def all_pass(filter_group, all_stock_info, start_index, end_index):
        success = True
        for filter in filter_group:
            if not filter(all_stock_info, start_index, end_index):
                success = False
                break
        return success

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
            success = False
            for filter_group in filters:
                if all_pass(filter_group, all_stock_info, start_index, end_index):
                    success = True
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
