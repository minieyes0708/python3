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

    def update_date(self, date):
        import json, re
        self.web.get(self.url % (date.year, date.month, date.day))
        result = json.loads(self.web.find_element_by_tag_name('pre').text)
        if 'data5' in result:
            for stock_info in result['data5']:
                values = {
                    'date_info': date,
                    'stock_id': stock_info[0],
                    'stock_name': stock_info[1],
                    'deal_stock_count': stock_info[2].replace(',',''),
                    'open_price': stock_info[5],
                    'highest_price': stock_info[6],
                    'lowest_price': stock_info[7],
                    'close_price': stock_info[8],
                    'rise_fall': re.sub('<.*?>', '', stock_info[9])
                }
                try:
                    float(values['open_price'])
                    float(values['rise_fall'])
                except ValueError:
                    continue
                if len(values['stock_id']) == 6 and values['stock_id'][0] == '7':
                    continue
                record = self.sql_cmd.format(**values)
                self.records[values['stock_id']] = record
