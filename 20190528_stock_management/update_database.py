# -*- coding=utf8 -*-
from WebController import WebController
from DBController import DBController
from datetime import timedelta, date


def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


with WebController() as web:
    with DBController() as db:
        web.select_date(date(2019, 1, 26))
        web.update_all_types()
