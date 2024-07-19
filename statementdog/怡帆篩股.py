import os, shutil, statementdog

# settings
take_count = None # set None to take all
dirname = 'evin-select-stocks'
filename = 'evin-select-stocks.txt'

# login
dog = statementdog.statementdog().login()

# returning the point just before turning
def find_next_turning_point(curv1, curv2, start_point):
    while start_point >= 0:
        if (curv1[start_point] - curv2[start_point]) * (curv1[start_point+1] - curv2[start_point+1]) < 0:
            return start_point
        else:
            start_point -= 1
    return start_point

# continue last round
if os.path.exists(filename):
    records = []
    keys = ('stockid', 'stockname')
    for line in open(filename):
        records.append(dict(zip(keys, line.strip().split())))
# new fresh start
else:
    if os.path.exists(dirname):
        shutil.rmtree(dirname)
    os.mkdir(dirname)
    records = dog.evin_select_stock()

skip = True
print('len(records) = ', len(records))
for i, record in enumerate(records):
    if record['stockid'] == '2432': skip = False
    if skip: continue
    print(f'goto {record["stockid"]}({i}/{len(records)})')
    try:
        [recent3months, _, recent12months] = dog.goto(record['stockid']).get_data_table()
    except RuntimeError as e:
        if str(e) == 'Page not found':
            continue
        else:
            raise
    if (
        len(recent3months) >= 4 and
        recent3months[-1] > recent3months[-2] and
        recent3months[-2] > recent3months[-3] and
        recent3months[-3] > recent3months[-4]
    ):
        output_filename = os.path.join(dirname, '{stockname} ({stockid}).jpg'.format(**record))
        dog.capture_monthly_revenue_yoy(record['stockid'], output_filename)
        print('added {stockname} ({stockid})'.format(**record))
    if take_count and i >= take_count - 1:
        break
records = records[i+1:]
if len(records):
    with open(filename, 'w') as file:
        for record in records:
            file.write('{stockid} {stockname}\n'.format(**record))
else:
    if os.path.exists(filename):
        os.remove(filename)

dog.web.quit()