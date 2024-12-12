from selenium.webdriver.common.by import By
class statementdog:
    def __init__(self):
        from selenium import webdriver
        self.web = webdriver.Chrome()
        self.web.get('https://statementdog.com')
    def login(self):
        self.waitfor(By.LINK_TEXT, '登入').click()
        self.waitfor(By.ID, 'user_email').send_keys('chenvey2@gmail.com')
        self.waitfor(By.ID, 'user_password').send_keys('shenfen520')
        self.web.find_element(By.CLASS_NAME, 'submit-btn').click()
        return self
    def select_stock(self, revenue_option = None):
        import time
        from selenium.webdriver.support.ui import Select
        ################
        # Select List1 #
        ################
        self.web.get('https://statementdog.com/screeners/custom')
        self.web.execute_script('importAll(0)')
        self.web.execute_script('$(".menu-title").removeClass("selected");')
        self.web.execute_script('$(".menu-title").eq(7).addClass("selected");')
        self.web.execute_script('$(".menu_wrapper").hide();')
        self.web.execute_script('$(".menu_wrapper").eq(7).show().find("li:visible").eq(0).trigger("click");')
        ########################
        # Additional Condition #
        ########################
        if revenue_option == '近三月營收年增率3個月內漲破近6月':
            index_element = self.web.find_element(By.ID, '營收年增率突破指標1')
            time_element = index_element.find_element(By.NAME, 'time')
            Select(time_element).select_by_value("3")
            self.web.execute_script('addIdx2("營收年增率突破指標1", "目前")')
        elif revenue_option == '近三月營收年增率3個月內漲破近12月':
            index_element = self.web.find_element(By.ID, '營收年增率突破指標2')
            time_element = index_element.find_element(By.NAME, 'time')
            Select(time_element).select_by_value("3")
            self.web.execute_script('addIdx2("營收年增率突破指標2", "目前")')
        ################
        # Start Select #
        ################
        self.web.find_element(By.LINK_TEXT, '開始選股').click()
        ##############
        # Select 台股 #
        ##############
        results = self.waitfor(By.CSS_SELECTOR, 'td.r-td2')
        self.web.find_element(By.XPATH, '//li[@data-country-type="tw"]').click()
        ###################
        # Extract Results #
        ###################
        results = self.web.find_elements(By.CSS_SELECTOR, 'td.r-td2')
        while len(results) == 0:
            time.sleep(1)
            results = self.web.find_elements_by_css_selector('td.r-td2')
        ###############
        # Get Records #
        ###############
        records = []
        keys = ('stockid', 'stockname')
        for td in results:
            records.append(dict(zip(keys, td.text.split())))
        return records
    def evin_select_stock(self):
        import time
        ################
        # Select List1 #
        ################
        results = self.waitfor(By.CSS_SELECTOR, 'button.navi-button-dropdown.navi-button-pick-stock')
        self.web.find_element(By.CSS_SELECTOR, 'button.navi-button-dropdown.navi-button-pick-stock').click()
        results = self.waitfor(By.LINK_TEXT, '自訂選股')
        self.web.find_element(By.LINK_TEXT, '自訂選股').click()
        # self.web.get('https://statementdog.com/screeners/custom')
        results = self.waitfor(By.LINK_TEXT, '清單3')
        self.web.find_element(By.LINK_TEXT, '清單3').click()
        self.web.execute_script('importAll(2)')
        self.web.execute_script('$(".menu-title").removeClass("selected");')
        self.web.execute_script('$(".menu-title").eq(7).addClass("selected");')
        self.web.execute_script('$(".menu_wrapper").hide();')
        self.web.execute_script('$(".menu_wrapper").eq(7).show().find("li:visible").eq(0).trigger("click");')
        ################
        # Start Select #
        ################
        self.web.find_element(By.LINK_TEXT, '開始選股').click()
        ##############
        # Select 台股 #
        ##############
        results = self.waitfor(By.CSS_SELECTOR, 'td.r-td2')
        self.web.find_element(By.XPATH, '//li[@data-country-type="tw"]').click()
        ###################
        # Extract Results #
        ###################
        results = self.web.find_elements(By.CSS_SELECTOR, 'td.r-td2')
        while len(results) == 0:
            time.sleep(1)
            results = self.web.find_elements_by_css_selector('td.r-td2')
        ###############
        # Get Records #
        ###############
        records = []
        keys = ('stockid', 'stockname')
        for td in results:
            records.append(dict(zip(keys, td.text.split())))
        return records
    def select_tracking(self):
        self.web.get('https://statementdog.com/feeds')
        div = self.waitfor(By.CLASS_NAME, 'stock-list')

        records = []
        keys = ('stockid', 'stockname')
        for ul in div.find_elements_by_tag_name('ul'):
            li = ul.find_element(By.CLASS_NAME, 'stock-id-name')
            records.append(dict(zip(keys, li.text.split())))
        return records
    def waitfor(self, by, *args):
        import time
        import selenium
        start = time.time()
        timeout = args['timeout'] if 'timeout' in args else 10
        while True:
            try:
                return self.web.find_element(by, *args)
            except selenium.common.exceptions.NoSuchElementException:
                print('waiting for ' + by + ' ' + ' '.join(str(v) for v in args))
                if time.time() - start > timeout:
                    if self.web.find_element(By.ID, 'content-title').text == '沒有這個頁面喔!':
                        raise RuntimeError('Page not found')
                time.sleep(1)
            except:
                raise
    def goto(self, stockid):
        self.web.get(f'https://statementdog.com/analysis/{stockid}/long-term-and-short-term-monthly-revenue-yoy')
        return self
    def getYoY(self, stockid):
        import time
        self.web.get(f'https://statementdog.com/analysis/{stockid}')
        info = self.web.find_elements_by_class_name('company-latest-valuation')
        while len(info) == 0:
            info = self.web.find_elements_by_class_name('company-latest-valuation')
            print('waiting company-latest-valuation')
            time.sleep(1)
        for tr in info[0].find_elements_by_tag_name('tr'):
            th = tr.find_elements_by_tag_name('th')[0]
            if 'YOY' in th.text:
                print('YOY = ' + tr.find_elements_by_tag_name('td')[0].text)
                return tr.find_elements_by_tag_name('td')[0].text
        raise RuntimeError("YOY Not Found")
    def get_data_table(self):
        import re
        data_table = self.waitfor(By.CSS_SELECTOR, "li#dataTable table")
        row_entries = data_table.find_elements(By.TAG_NAME, "tr")

        take_index = []
        recent3months = [td.text for td in row_entries[1].find_elements(By.TAG_NAME, "td")]
        recent6months = [td.text for td in row_entries[2].find_elements(By.TAG_NAME, "td")]
        recent12months = [td.text for td in row_entries[3].find_elements(By.TAG_NAME, "td")]
        for i in range(len(recent3months)):
            if recent3months[i] != '無' and recent6months[i] != '無' and recent12months[i] != '無':
                take_index.append(i)
        check_float = re.compile(r"^[-+]?[0-9]*\.?[0-9]+$")
        recent3months = [float(recent3months[i].replace(',', '')) if check_float.match(recent3months[i]) else float('nan') for i in take_index]
        recent6months = [float(recent6months[i].replace(',', '')) if check_float.match(recent6months[i]) else float('nan') for i in take_index]
        recent12months = [float(recent12months[i].replace(',', '')) if check_float.match(recent12months[i]) else float('nan') for i in take_index]
        return [recent3months, recent6months, recent12months]
    def capture_monthly_revenue_yoy(self, stock_id, filename):
        self.goto(stock_id).waitfor(By.ID, 'report')
        self.web.save_screenshot(filename)

class record_handler:
    def __init__(self):
        import shelve
        folder = 'D:/minieyes/program/python/'
        self.todo = shelve.open(folder + 'statementdog/todo.txt')
        self.expire = shelve.open(folder + 'statementdog/expire.txt')
    def add_todo(self, records, condition = None):
        from datetime import datetime
        now = datetime.now()
        valid_records = []
        for record in records:
            if not record['stockid'] in self.expire or self.expire[record['stockid']] < now:
                valid_records.append(record)
        for index, record in enumerate(valid_records):
            print(f'{index+1}/{len(valid_records)}')
            if condition and condition(record):
                self.todo[record['stockid']] = record
    def add_expire(self, record, expire_month):
        from datetime import datetime
        from dateutil.relativedelta import relativedelta
        self.expire[record['stockid']] = (datetime.now() + relativedelta(months=expire_month)).replace(day=1)
    def show_todo(self):
        for key, value in self.todo.items():
            print(value)
    def show_expire(self, stockid = None):
        if stockid:
            if stockid not in self.expire:
                print('stockid not fond')
            else:
                print(stockid, self.expire[stockid])
        else:
            for key, value in self.expire.items():
                print(key, value)

class interactive_console:
    def __init__(self, dog, handler):
        self.dog = dog
        self.handler = handler

        self.pars = []
        self.query = ''
        self.stockid = ''
        self.commands = []
        self.quit_commands = ['exit', 'quit', 'bye', 'q']

    def print_help(self):
        print('0: [update] todo')
        print('1: [show] todo')
        print('2: [set] stockid + goto')
        print('3: [goto] stock')
        print('4: [expire] stock + remove + show')
        print('5: [remove] stock')
        print('6: [show_expire]')
        print('7: [update2] all list1')
        print('8: [update3] tracking')
        print('9: [clear] todo')
        print('10:[turning] find all turning stock and add to todo')
        print(f'current id {self.stockid} in {len(self.handler.todo)} stocks')
    def get_commands(self):
        if len(self.commands) == 0:
            self.commands = [v.strip() for v in input('> ').strip().split(',')]
    def parse_next_command(self):
        self.pars = [v.strip() for v in self.commands[0].split()]
        self.commands = self.commands[1:]
        if len(self.pars): self.query = self.pars[0]

    def goto_last_stock(self):
        if len(self.handler.todo):
            self.stockid = list(self.handler.todo.keys())[-1]
            self.dog.goto(self.stockid)
    def update(self):
        self.handler.add_todo(self.dog.select_stock('近三月營收年增率3個月內漲破近6月'))
        self.handler.add_todo(self.dog.select_stock('近三月營收年增率3個月內漲破近12月'))
        self.handler.show_todo()
        self.goto_last_stock()
    def show(self):
        self.handler.show_todo()
    def set(self):
        if len(self.pars) > 1:
            self.stockid = self.pars[1]
        else:
            self.stockid = input('stock id = ').strip()
        self.dog.goto(self.stockid)
    def goto(self):
        self.dog.goto(self.stockid)
    def expire(self):
        expire_month = eval(self.pars[1]) if len(self.pars) > 1 else eval(input('expire months = ').strip())
        self.handler.add_expire(self.handler.todo[self.stockid], expire_month)
        self.remove()
    def remove(self):
        del self.handler.todo[self.stockid]
        self.handler.show_todo()
        self.goto_last_stock()
    def show_expire(self):
        self.handler.show_expire(self.pars[1] if len(self.pars) > 1 else None)
    def update2(self):
        self.handler.add_todo(self.dog.select_stock(''),
                condition = (lambda record: self.dog.getYoY(record['stockid']) != '無'))
        self.handler.show_todo()
        self.goto_last_stock()
    def update3(self):
        for record in self.dog.select_tracking():
            self.handler.todo[record['stockid']] = record
        handler.show_todo()
        self.goto_last_stock()
    def clear(self):
        handler.todo.clear()
    def turning(self):
        def find_next_turning_point(curv1, curv2, start_point):
            while start_point >= 0:
                if (curv1[start_point] - curv2[start_point]) * (curv1[start_point+1] - curv2[start_point+1]) < 0:
                    return start_point
                else:
                    start_point -= 1
            return start_point

        records = self.dog.select_stock('近三月營收年增率3個月內漲破近6月')
        print('len(records) = ', len(records))
        for i, record in enumerate(records):
            print(f'goto {record["stockid"]}({i}/{len(records)})')
            self.dog.goto(record['stockid'])
            [recent3months, _, recent12months] = self.dog.get_data_table()
            total_months = len(recent3months)
            if recent3months[-1] > recent12months[-1]:
                tp1 = find_next_turning_point(recent3months, recent12months, total_months - 2)
                tp2 = find_next_turning_point(recent3months, recent12months, tp1-1)
                if total_months - tp1 < 5 and tp1 - tp2 > 10:
                    self.handler.todo[record['stockid']] = record
                    print(f'added {record["stockid"]}')
        self.goto_last_stock()

    def mainloop(self):
        while self.query not in self.quit_commands:
            self.print_help()
            self.get_commands()
            self.parse_next_command()

            try:
                getattr(self, self.query)()
            except AttributeError:
                pass

if __name__ == '__main__':
    handler = record_handler()
    dog = statementdog()
    dog.login()

    console = interactive_console(dog, handler)
    console.mainloop()

    #  print('press any key to continue')
    #  input()
