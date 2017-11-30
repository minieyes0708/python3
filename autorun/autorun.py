# -*- coding=cp950 -*-
import os

os.chdir(r'C:\Program Files\Python36\minieyes\autorun')
exec(open('LoanNotify.py').read(), globals())

os.chdir(r"C:\Program Files (x86)\No-IP")
os.system('START "" DUC40.exe')
