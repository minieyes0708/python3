import os, re

EXTRACT_CMD = '"C:\\Program Files\\7-Zip\\7z.exe" x "%s.rar" -p%s'

os.chdir(r'D:\Downloads')

folders = [file for file in os.listdir('.') if os.path.isdir(file)]
for folder in folders:
    os.chdir(folder)
    if os.path.isfile('password.txt'):
        password = open('password.txt').read()
        with open('extract.bat', 'w') as file:
            file.write(EXTRACT_CMD % (folder, password))
    os.chdir('..')
