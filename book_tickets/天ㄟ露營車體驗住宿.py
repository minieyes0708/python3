import tkinter as tk
from tkinter import ttk


class Main:
    def __init__(self):
        from selenium import webdriver
        global web
        web = webdriver.Chrome()
        web.get("http://www.kitravel.com.tw/booking/tan.a.camper/")
        window = MainWindow()
        window.mainloop()


class MainWindow:
    def __init__(self):
        self.window = None
        self.btnReset = None
        self.tabControl = None
        self.tabPage1 = None
        self.tabPage2 = None
        self.room_types = (
            '天ㄟ1號(可帶寵物限帶3隻)', '天ㄟ2號(可帶寵物限帶3隻)', '天ㄟ3號', '天ㄟ5號', '天ㄟ7號',
            '天ㄟ8號(可帶寵物限帶3隻)', '天ㄟ9號(可帶寵物限帶3隻)', '天ㄟ10號', '天ㄟ11號', '天ㄟ12號',
            '加人(大人)', '加小孩(7~12歲)', '帶寵物，收清潔費(1隻)'
        )

        self.create_window()

        self.txtDate = tk.StringVar()
        self.txtDate.set('2019-11-13')
        self.txtAdult = tk.StringVar()
        self.txtAdult.set('2')
        self.txtChild = tk.StringVar()
        self.txtChild.set('1')
        self.txtRoomType = tk.StringVar()
        self.txtDays = tk.StringVar()
        self.txtDays.set('1')
        self.txtAddChild = tk.StringVar()
        self.txtAddChild.set('1')

        self.txtBookName = tk.StringVar()
        self.txtBookName.set('王聖雰')
        self.intBookGender = tk.IntVar()
        self.intBookGender.set(1)
        self.txtBookCellPhone = tk.StringVar()
        self.txtBookCellPhone.set('0932871908')
        self.txtBookEmail = tk.StringVar()
        self.txtBookEmail.set('shenfen@msn.com')
        self.txtBookArriveDate = tk.StringVar()
        self.txtBookArriveDate.set('2020-03-01')
        self.txtBookArriveTime = tk.StringVar()
        self.txtBookArriveTime.set('03:30 AM')
        self.txtBookAddress = tk.StringVar()
        self.txtBookAddress.set('新竹市關新路19巷65號8樓')
        self.txtBookMessage = tk.StringVar()
        self.txtBookMessage.set('')

        self.create_reset_button()
        self.create_tab_control()

    def create_window(self):
        self.window = tk.Tk()
        self.window.attributes("-topmost", True)
        self.window.title = '天ㄟ露營車體驗住宿'

    def create_reset_button(self):
        self.btnReset = tk.Button(self.window, text='重連主頁', command=self.back_to_homepage, fg='red').pack(expand=1, fill='both', padx=3, pady=3)

    def create_tab_control(self):
        MainTabControl(self)

    def mainloop(self):
        self.window.mainloop()

    @staticmethod
    def back_to_homepage():
        global web
        web.get("http://www.kitravel.com.tw/booking/tan.a.camper/")


class MainTabControl:
    def __init__(self, window):
        self.window = window
        window.tabControl = ttk.Notebook(window.window)
        window.tabControl.pack(expand=1, fill='both')
        TabPage1(window)
        TabPage2(window)
        TabPage3(window)
        TabPage4(window)
        TabPage5(window)


class TabPage:
    def __init__(self):
        self.window = None
        self.page = None

    def create_next_step(self, callback):
        tk.Button(self.page, text='下一步', command=callback).grid(row=0, columnspan=5, sticky='we', padx=3, pady=3)

    def add_to_tab_control(self, title):
        self.window.tabControl.add(self.page, text=title)

    def initialize(self, window, title, callback):
        self.window = window
        self.page = ttk.Frame(window.tabControl)

        self.create_next_step(callback)
        self.add_to_tab_control(title)

        return self.page

    def click_next_step(self):
        global web
        web.find_element_by_id('btnNext').click()
        self.window.tabControl.select(self.window.tabControl.index(self.window.tabControl.select()) + 1)


class TabPage1(TabPage):
    def __init__(self, window):
        window.tabPage1 = self.initialize(window, '基本需求', self.fill_basic_needs)
        self.page.columnconfigure(2, weight=1)
        self.page.columnconfigure(4, weight=1)

        self.create_date()
        self.create_people()
        self.create_next_step(self.fill_basic_needs)

    def create_date(self):
        tk.Label(self.page, text='挑選入住日期').grid(row=1, column=0)
        tk.Entry(self.page, textvariable=self.window.txtDate).grid(row=1, column=1, columnspan=4, sticky='we', padx=3, pady=3)

    def create_people(self):
        tk.Label(self.page, text='入住人數').grid(row=2, column=0, sticky='e')
        tk.Label(self.page, text='成人').grid(row=2, column=1)
        tk.Entry(self.page, textvariable=self.window.txtAdult).grid(row=2, column=2, padx=3, pady=3, sticky='we')
        tk.Label(self.page, text='小孩').grid(row=2, column=3)
        tk.Entry(self.page, textvariable=self.window.txtChild).grid(row=2, column=4, padx=3, pady=3, sticky='we')

    def fill_basic_needs(self):
        global web
        web.find_element_by_id('checkin').clear()
        web.find_element_by_id('checkin').send_keys(self.window.txtDate.get())
        web.find_element_by_id('adult').clear()
        web.find_element_by_id('adult').send_keys(self.window.txtAdult.get())
        web.find_element_by_id('child').clear()
        web.find_element_by_id('child').send_keys(self.window.txtChild.get())
        self.click_next_step()


class TabPage2(TabPage):
    def __init__(self, window):
        window.tabPage2 = self.initialize(window, '訂房', self.book_room)
        self.page.columnconfigure(1, weight=1)

        self.create_date()
        self.create_room_type()
        self.create_people()

    def create_date(self):
        tk.Label(self.page, text='日期').grid(row=1, column=0)
        tk.Entry(self.page, textvariable=self.window.txtDate).grid(row=1, column=1, sticky='we', padx=3, pady=3)

    def create_room_type(self):
        tk.Label(self.page, text='房型').grid(row=2, column=0)
        room_type_combobox = ttk.Combobox(self.page, textvariable=self.window.txtRoomType)
        room_type_combobox['values'] = self.window.room_types
        room_type_combobox.grid(row=2, column=1, sticky='we', padx=3, pady=3)
        room_type_combobox.current(0)

    def create_people(self):
        tk.Label(self.page, text='天數').grid(row=3, column=0)
        tk.Entry(self.page, textvariable=self.window.txtDays).grid(row=3, column=1, sticky='we', padx=3, pady=3)

    def book_room(self):
        from datetime import datetime
        global web
        target_date = datetime.strptime(self.window.txtDate.get(), '%Y-%m-%d')
        web.execute_script("addCart('wd%d%02d%02d%d',%d);" % (
            target_date.year, target_date.month, target_date.day,
            self.window.room_types.index(self.window.txtRoomType.get()) + 1,
            int(self.window.txtDays.get())
        ))
        self.click_next_step()


class TabPage3(TabPage):
    def __init__(self, window):
        window.tabPage3 = self.initialize(window, '訂房須知', self.need_to_know)
        self.page.columnconfigure(0, weight=1)

    def need_to_know(self):
        self.click_next_step()


class TabPage4(TabPage):
    def __init__(self, window):
        window.tabPage4 = self.initialize(window, '加幼兒', self.add_child)
        self.page.columnconfigure(1, weight=1)

        self.create_add_child()

    def create_add_child(self):
        tk.Label(self.page, text='加幼兒(7歲以下)').grid(row=1, column=0)
        tk.Entry(self.page, textvariable=self.window.txtAddChild).grid(row=1, column=1, sticky='we', padx=3, pady=3)

    def add_child(self):
        global web
        element = web.find_element_by_id('pk_a_1')
        value = self.window.txtAddChild.get()
        web.execute_script('arguments[0].setAttribute("value", arguments[1])', element, value)
        self.click_next_step()


class TabPage5(TabPage):
    def __init__(self, window):
        window.tabPage5 = self.initialize(window, '訂單資訊', self.book_info)
        self.page.columnconfigure(2, weight=1)

        self.initialize_components()

    def initialize_components(self):
        tk.Label(self.page, text='姓名').grid(row=1, column=0)
        tk.Entry(self.page, textvariable=self.window.txtBookName).grid(row=1, column=1, columnspan=2, sticky='we')
        tk.Label(self.page, text='性別').grid(row=2, column=0)
        tk.Radiobutton(self.page, text='先生', variable=self.window.intBookGender, value=0).grid(row=2, column=1)
        tk.Radiobutton(self.page, text='小姐', variable=self.window.intBookGender, value=1).grid(row=2, column=2)
        tk.Label(self.page, text='手機').grid(row=3, column=0)
        tk.Entry(self.page, textvariable=self.window.txtBookCellPhone).grid(row=3, column=1, columnspan=2, sticky='we')
        tk.Label(self.page, text='Email').grid(row=4, column=0)
        tk.Entry(self.page, textvariable=self.window.txtBookEmail).grid(row=4, column=1, columnspan=2, sticky='we')
        tk.Label(self.page, text='到達時間').grid(row=5, column=0)
        tk.Entry(self.page, textvariable=self.window.txtBookArriveDate).grid(row=5, column=1)
        tk.Entry(self.page, textvariable=self.window.txtBookArriveTime).grid(row=5, column=2)
        tk.Label(self.page, text='地址').grid(row=6, column=0)
        tk.Entry(self.page, textvariable=self.window.txtBookAddress).grid(row=6, column=1, columnspan=2, sticky='we')
        tk.Label(self.page, text='留言').grid(row=7, column=0)
        tk.Entry(self.page, textvariable=self.window.txtBookMessage).grid(row=7, column=1, columnspan=2, sticky='we')

    def book_info(self):
        web.find_element_by_id('fuserName').clear()
        web.find_element_by_id('fuserName').send_keys(self.window.txtBookName.get())
        if self.window.intBookGender.get() == 0:
            web.find_element_by_id('fgender1').click()
        else:
            web.find_element_by_id('fgender2').click()
        web.find_element_by_id('fphone').clear()
        web.find_element_by_id('fphone').send_keys(self.window.txtBookCellPhone.get())
        web.find_element_by_id('femail').clear()
        web.find_element_by_id('femail').send_keys(self.window.txtBookEmail.get())
        web.find_element_by_id('farrivalDate').clear()
        web.find_element_by_id('farrivalDate').send_keys(self.window.txtBookArriveDate.get())
        web.find_element_by_id('timepicker1').clear()
        web.find_element_by_id('timepicker1').send_keys(self.window.txtBookArriveTime.get())
        web.find_element_by_id('faddress').clear()
        web.find_element_by_id('faddress').send_keys(self.window.txtBookAddress.get())
        web.find_element_by_id('fnote').clear()
        web.find_element_by_id('fnote').send_keys(self.window.txtBookMessage.get())
        # self.click_next_step()

if __name__ == '__main__':
    Main()
