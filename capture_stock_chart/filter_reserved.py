import sys

sys.path.append(r'C:\Program Files\Python36\minieyes\20190528_stock_management')

from DBController import DBController

with open('reserved.txt', 'r') as file:
    reserved = list(set([int(stock_id.strip()) for stock_id in file.readlines()]))

with DBController() as db:
    for stock_id in reserved:
        stock_info = db.get_stock_info_by_id(stock_id)
        rise_fall = [float(info['rise_fall']) for info in stock_info]
        if all(map(lambda x: x < 0, rise_fall[-3:])):
            print(stock_id, stock_info[0]['stock_name'])
