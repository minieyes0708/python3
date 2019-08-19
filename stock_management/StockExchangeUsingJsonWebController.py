# -*- coding=utf8 -*-
class StockExchangeUsingJsonWebController:
    def __init__(self):
        self.web = None
        self.sql_cmd = '''
        INSERT IGNORE INTO `everyday_close_info` VALUES(NULL,
        "{date_info}", "{stock_id}", "{stock_name}", {deal_stock_count}, 
        "{open_price}", "{highest_price}", "{lowest_price}", "{close_price}", "{rise_fall}")
        '''
        self.records = dict()
        self.url = 'http://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date=%d%02d%02d&type=ALL'

        self.result = None
        self.data_group = 'data5'

    def open(self):
        from selenium import webdriver
        self.web = webdriver.Chrome()

    def __enter__(self):
        self.open()
        return self

    def close(self):
        self.web.quit()

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()

    def find_data_group(self):
        for key in self.result.keys():
            try:
                if self.result[key][0][0] == "0050":
                    self.data_group = key
                    return True
            except KeyError:
                continue
        return False

    def update_date(self, date):
        import json, re
        self.web.implicitly_wait(300)
        self.web.get(self.url % (date.year, date.month, date.day))
        self.result = json.loads(self.web.find_element_by_tag_name('pre').text)
        if self.find_data_group() == False:
            print('Cannot Find Data Group')
            return
        for stock_info in self.result[self.data_group]:
            values = {
                'date_info': date,
                'stock_id': stock_info[0],
                'stock_name': stock_info[1],
                'deal_stock_count': stock_info[2].replace(',',''),
                'open_price': stock_info[5],
                'highest_price': stock_info[6],
                'lowest_price': stock_info[7],
                'close_price': stock_info[8],
                'rise_fall': re.sub('<.*?>', '', stock_info[9]) + stock_info[10]
            }
            try:
                float(values['open_price'])
                float(values['rise_fall'])
            except ValueError:
                continue
            if (
                    'X' in values['stock_id'] or
                    'P' in values['stock_id'] or
                    re.match(r'.*[購展]\d\d', values['stock_name'])
            ):
                continue
            record = self.sql_cmd.format(**values)
            self.records[values['stock_id']] = record
