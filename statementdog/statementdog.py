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
        self.web.get('https://statementdog.com/screeners/custom')
        self.web.execute_script('importAll(0)')
        self.web.execute_script('$(".menu-title").removeClass("selected");')
        self.web.execute_script('$(".menu-title").eq(7).addClass("selected");')
        self.web.execute_script('$(".menu_wrapper").hide();')
        self.web.execute_script('$(".menu_wrapper").eq(7).show().find("li:visible").eq(0).trigger("click");')
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
        self.web.find_element_by_link_text('開始選股').click()
        results = self.waitfor('find_elements_by_css_selector', 'td.r-td2')
        while len(results) == 0:
            time.sleep(1)
            results = self.web.find_elements_by_css_selector('td.r-td2')
        records = []
        keys = ('stockid', 'stockname')
        for td in results:
            records.append(dict(zip(keys, td.text.split())))
        return records
    def waitfor(self, attrname, *args):
        import time
        import selenium
        while True:
            try:
                return self.web.__getattribute__(attrname)(*args)
            except selenium.common.exceptions.NoSuchElementException:
                time.sleep(1)
            except:
                raise
    def goto(self, stockid):
        self.web.get(f'https://statementdog.com/analysis/{stockid}/long-term-and-short-term-monthly-revenue-yoy')

class record_handler:
    def __init__(self):
        import shelve
        self.todo = shelve.open('statementdog/todo.txt')
        self.expire = shelve.open('statementdog/expire.txt')
    def add_todo(self, records):
        from datetime import datetime
        now = datetime.now()
        for record in records:
            if not record['stockid'] in self.expire or self.expire[record['stockid']] < now:
                self.todo[record['stockid']] = record
    def add_expire(self, record, expire_month):
        from datetime import datetime
        from dateutil.relativedelta import relativedelta
        self.expire[record['stockid']] = datetime.now() + relativedelta(months=expire_month)
    def show_todo(self):
        for key, value in self.todo.items():
            print(value)
    def show_expire(self):
        for key, value in self.expire.items():
            print(key, value)

if __name__ == '__main__':
    handler = record_handler()
    dog = statementdog()
    dog.login()

    query = ''
    stockid = ''
    commands = ''
    while query != 'exit' and query != 'quit' and query != 'bye' and query != 'q':
        print('0: [update] todo')
        print('1: [show] todo')
        print('2: [set] stockid + goto')
        print('3: [goto] stock')
        print('4: [expire] stock + remove + show')
        print('5: [remove] stock')
        print('6: [show_expire]')
        print(f'current id {stockid} in {len(handler.todo)} stocks')
        if len(commands) == 0:
            commands = [v.strip() for v in input('> ').strip().split(',')]
        pars = [v.strip() for v in commands[0].split()]
        commands = commands[1:]
        query = pars[0]
        if query == '0' or query == 'update':
            records = dog.select_stock('近三月營收年增率3個月內漲破近6月')
            handler.add_todo(records)
            records = dog.select_stock('近三月營收年增率3個月內漲破近12月')
            handler.add_todo(records)
        elif query == '1' or query == 'show':
            handler.show_todo()
        elif query == '2' or query == 'set':
            if len(pars) > 1:
                stockid = pars[1]
            else:
                stockid = input('stock id = ').strip()
            dog.goto(stockid)
        elif query == '3' or query == 'goto':
            dog.goto(stockid)
        elif query == '4' or query == 'expire':
            if len(pars) > 1:
                expire_month = eval(pars[1])
            else:
                expire_month = eval(input('expire months = ').strip())
            handler.add_expire(handler.todo[stockid], expire_month)
            del handler.todo[stockid]
            handler.show_todo()
        elif query == '5' or query == 'remove':
            del handler.todo[stockid]
        elif query == '6' or query == 'show_expire':
            handler.show_expire()

    #  print('press any key to continue')
    #  input()
