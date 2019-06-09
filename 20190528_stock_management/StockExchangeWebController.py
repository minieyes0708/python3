# -*- coding=utf8 -*-
class StockExchangeWebController:
    def __init__(self):
        self.web = None
        self.sql_cmd = '''
        INSERT IGNORE INTO `everyday_close_info` VALUES(NULL,
        "{date_info}", "{stock_id}", "{stock_name}", {deal_stock_count}, 
        "{open_price}", "{highest_price}", "{lowest_price}", "{close_price}", "{rise_fall}")
        '''
        self.records = dict()

    def open(self):
        from selenium import webdriver
        self.web = webdriver.Chrome()
        self.web.get('http://www.twse.com.tw/zh/page/trading/exchange/MI_INDEX.html')

    def __enter__(self):
        self.open()
        return self

    def close(self):
        self.web.quit()

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()

    def is_no_records(self):
        if '很抱歉' in self.web.find_element_by_id('result-message').text:
            return True
        else:
            return False

    def wait_page_loading(self):
        rpt_tbl = self.web.find_element_by_id('report-table1')
        while not rpt_tbl.is_displayed():
            if '很抱歉' in self.web.find_element_by_id('result-message').text:
                break

    def select_show_all_records(self):
        import selenium
        from selenium.webdriver.support.ui import Select
        try:
            select_rpt_tbl_len = Select(self.web.find_element_by_name('report-table1_length'))
            select_rpt_tbl_len.select_by_visible_text('全部')
        except selenium.common.exceptions.NoSuchElementException:
            pass

    def get_selected_date(self):
        from datetime import date
        from selenium.webdriver.support.ui import Select
        year = int(Select(self.web.find_element_by_name('yy')).all_selected_options[0].get_attribute('value'))
        month = int(Select(self.web.find_element_by_name('mm')).all_selected_options[0].get_attribute('value'))
        day = int(Select(self.web.find_element_by_name('dd')).all_selected_options[0].get_attribute('value'))
        return date(year, month, day)

    def update_current_page(self):
        self.select_show_all_records()
        date_info = self.get_selected_date()
        rpt_tbl = self.web.find_element_by_id('report-table1')
        tbl_head = rpt_tbl.find_element_by_tag_name('thead')
        if '證券代號' in tbl_head.text:
            header_row = tbl_head.find_elements_by_tag_name('tr')[1]
            header_texts = [th.text for th in header_row.find_elements_by_tag_name('th')]
            stock_id_col = header_texts.index('證券代號')
            stock_name_col = header_texts.index('證券名稱')
            deal_stock_count_col = header_texts.index('成交股數')
            open_price_col = header_texts.index('開盤價')
            highest_price_col = header_texts.index('最高價')
            lowest_price_col = header_texts.index('最低價')
            close_price_col = header_texts.index('收盤價')
            rise_fall_col1 = header_texts.index('漲跌(+/-)')
            rise_fall_col2 = header_texts.index('漲跌價差')
            tbody = rpt_tbl.find_element_by_tag_name('tbody')
            for tr in tbody.find_elements_by_tag_name('tr'):
                tds = tr.find_elements_by_tag_name('td')
                if len(tds) < rise_fall_col2:
                    continue
                values = {
                    'date_info': date_info,
                    'stock_id': tds[stock_id_col].text,
                    'stock_name': tds[stock_name_col].text,
                    'deal_stock_count': int(tds[deal_stock_count_col].text.replace(',', '')),
                    'open_price': tds[open_price_col].text,
                    'highest_price': tds[highest_price_col].text,
                    'lowest_price': tds[lowest_price_col].text,
                    'close_price': tds[close_price_col].text,
                    'rise_fall': tds[rise_fall_col1].text + tds[rise_fall_col2].text
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

    def select_type_by_index(self, index):
        from selenium.webdriver.support.ui import Select
        select_type = Select(self.web.find_element_by_name('type'))
        select_type.select_by_index(index)

    def get_all_type_count(self):
        from selenium.webdriver.support.ui import Select
        select_type = Select(self.web.find_element_by_name('type'))
        return len(select_type.options)

    def select_date(self, target_date):
        from selenium.webdriver.support.ui import Select
        Select(self.web.find_element_by_name('yy')).select_by_value(str(target_date.year))
        Select(self.web.find_element_by_name('mm')).select_by_value(str(target_date.month))
        Select(self.web.find_element_by_name('dd')).select_by_value(str(target_date.day))

    def search(self):
        self.web.find_element_by_link_text('查詢').click()

    def is_holiday(self):
        self.select_type_by_index(19)
        self.search()
        self.wait_page_loading()
        if self.is_no_records():
            return True
        else:
            return False

    def update_all_types(self):
        from selenium.webdriver.support.ui import Select
        if self.is_holiday():
            print(str(self.get_selected_date()) + ' is holiday')
            return
        select_type = Select(self.web.find_element_by_name('type'))
        total_count = len(select_type.options)
        for typeIndex in range(18, total_count):
            print('processing {0} ({1}/{2})'.format(select_type.options[typeIndex].text, typeIndex, total_count))
            select_type.select_by_index(typeIndex)
            self.search()
            self.wait_page_loading()
            if self.is_no_records():
                continue
            self.update_current_page()
