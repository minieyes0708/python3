# -*- coding=cp950 -*-
import os, sys
from datetime import datetime

os.chdir(r'C:\Program Files\Python36\minieyes')
sys.path.append('.')

today = datetime.now()
if today.day >= 14 and today.day <= 18:
    lastdate = ''
    if os.path.isfile('./autorun/LoanNotify.txt'):
        with open('./autorun/LoanNotify.txt') as file:
            lastdate = file.readline()
    if lastdate != str(today.year) + str(today.month):
        from utilities.miniSendMail import miniSendMail
        mail = miniSendMail()
        mail.send('繳車貸', '餓死抬頭')
        with open('./autorun/LoanNotify.txt', 'w') as file:
            file.write(str(today.year) + str(today.month))
