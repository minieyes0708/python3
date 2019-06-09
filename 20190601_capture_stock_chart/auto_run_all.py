import sys

sys.path.append(r'C:\Program Files\Python36\minieyes\20190528_stock_management')

import update_database
import filter_stock
with open('stocks.txt', 'w') as file:
    file.write('\n'.join(filter_stock.passed_stocks))

import capture_stocks
