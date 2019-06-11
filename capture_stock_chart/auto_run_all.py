from minieyes.stock_management.update_database import *
from minieyes.stock_management.filter_stock import *
from minieyes.capture_stock_chart.capture_stocks import *

update_database()
passed_stocks = filter_stock()
with open('stocks.txt', 'w') as file:
    file.write('\n'.join(passed_stocks))
capture_stocks()
