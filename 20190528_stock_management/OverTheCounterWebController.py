# -*- coding=utf8 -*-
class OverTheCounterWebController:
    def __init__(self):
        self.web = None
        self.sql_cmd = '''
        INSERT IGNORE INTO `everyday_close_info` VALUES(NULL,
        "{date_info}", "{stock_id}", "{stock_name}", {deal_stock_count}, 
        "{open_price}", "{highest_price}", "{lowest_price}", "{close_price}", "{rise_fall}")
        '''
        self.records = dict()
        self.url = 'https://www.tpex.org.tw/web/stock/aftertrading/otc_quotes_no1430/stk_wn1430_result.php?l=zh-tw&d=%d/%02d/%02d&se=AL'

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
        import json
        self.web.get(self.url % (date.year - 1911, date.month, date.day))
        result = json.loads(self.web.find_element_by_tag_name('pre').text)
        for stock_info in result['aaData']:
            values = {
                'date_info': date,
                'stock_id': stock_info[0],
                'stock_name': stock_info[1],
                'deal_stock_count': stock_info[7].replace(',',''),
                'open_price': stock_info[4],
                'highest_price': stock_info[5],
                'lowest_price': stock_info[6],
                'close_price': stock_info[2],
                'rise_fall': stock_info[3]
            }
            try:
                float(values['open_price'])
                float(values['rise_fall'])
            except ValueError:
                continue
            record = self.sql_cmd.format(**values)
            self.records[values['stock_id']] = record
