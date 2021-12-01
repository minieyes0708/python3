class statementdog:
    def __init__(self):
        from selenium import webdriver
        self.web = webdriver.Chrome()
        self.web.get('https://statementdog.com')
    def login(self):
        self.waitfor('find_element_by_link_text', '登入').click()
        self.waitfor('find_element_by_id', 'user_email').send_keys('chenvey2@gmail.com')
        self.waitfor('find_element_by_id', 'user_password').send_keys('shenfen520')
        self.web.find_element_by_class_name('submit-btn').click()
    def select_stock(self, revenue_option):
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
            index_element = self.web.find_element_by_id('營收年增率突破指標1')
            time_element = index_element.find_element_by_name('time')
            Select(time_element).select_by_value("3")
            self.web.execute_script('addIdx2("營收年增率突破指標1", "目前")')
        elif revenue_option == '近三月營收年增率3個月內漲破近12月':
            index_element = self.web.find_element_by_id('營收年增率突破指標2')
            time_element = index_element.find_element_by_name('time')
            Select(time_element).select_by_value("3")
            self.web.execute_script('addIdx2("營收年增率突破指標2", "目前")')
        ################
        # Start Select #
        ################
        self.web.find_element_by_link_text('開始選股').click()
        ###################
        # Extract Results #
        ###################
        results = self.waitfor('find_elements_by_css_selector', 'td.r-td2')
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
        div = self.waitfor('find_element_by_class_name', 'stock-list')

        records = []
        keys = ('stockid', 'stockname')
        for ul in div.find_elements_by_tag_name('ul'):
            li = ul.find_element_by_class_name('stock-id-name')
            records.append(dict(zip(keys, li.text.split())))
        return records
    def waitfor(self, attrname, *args):
        import time
        import selenium
        while True:
            try:
                return self.web.__getattribute__(attrname)(*args)
            except selenium.common.exceptions.NoSuchElementException:
                print('waiting for ' + attrname + ' ' + ' '.join(str(v) for v in args))
                time.sleep(1)
            except:
                raise
    def goto(self, stockid):
        self.web.get(f'https://statementdog.com/analysis/{stockid}/long-term-and-short-term-monthly-revenue-yoy')
    def getYoY(self, stockid):
        import time
        self.web.get(f'https://statementdog.com/analysis/{stockid}')
        info = self.web.find_elements_by_class_name('company-latest-valuation-container')
        while len(info) == 0:
            info = self.web.find_elements_by_class_name('company-latest-valuation-container')
            print('waiting company-latest-valuation-container')
            time.sleep(1)
        for tr in info[0].find_elements_by_tag_name('tr'):
            th = tr.find_elements_by_tag_name('th')[0]
            if 'YOY' in th.text:
                print('YOY = ' + tr.find_elements_by_tag_name('td')[0].text)
                return tr.find_elements_by_tag_name('td')[0].text
        raise RuntimeError("YOY Not Found")

class record_handler:
    def __init__(self):
        import shelve
        self.todo = shelve.open('statementdog/todo.txt')
        self.expire = shelve.open('statementdog/expire.txt')
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
        self.handler.add_todo(dog.select_stock('近三月營收年增率3個月內漲破近12月'))
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
