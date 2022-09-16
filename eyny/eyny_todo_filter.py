#!/usr/bin/env python3
from minieyes.eyny.eyny import eyny

eyny = eyny()
total = eyny.count()
eyny.set_mega_links((
    'https://mega.nz',
    'http://www.xunniupan',
    'https://rosefile.net',
     # 'https://katfile.com',
    'http://drives.google',
    'https://drives.google',
))

file = open('./eyny/todo_filter.txt', 'a', encoding='UTF-8')
for index, title, link in eyny.loop_and_remove():
    print('========== %d/%d ==========' % (index, total))
    print('{0}({1})'.format(title.decode('utf8'), link))
    eyny.goto(link)
    eyny.confirm18()

    url, passwd = eyny.get_mega_links(), eyny.get_passwords()
    urls, passwds = '\n'.join(url), '\n'.join(passwd)

    if len(url) != 0:
        file.write('{\n')
        file.write(
            '========== %d/%d ==========\nlink = %s\n%s\n%s\n' %
            (index, total, link, urls, passwds))
        print('%s\n%s' % (urls, passwds))
        file.write('}\n')
file.close()
