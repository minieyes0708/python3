import os, shutil, statementdog

# settings
take_count = None # set None to take all
dirname = 'monthly-revenue-yoy-turning'
filename = 'monthly-revenue-yoy-turning.txt'

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
    records = dog.select_stock()

print('len(records) = ', len(records))
for i, record in enumerate(records):
    print(f'goto {record["stockid"]}({i}/{len(records)})')
    [recent3months, _, recent12months] = dog.goto(record['stockid']).get_data_table()
    total_months = len(recent3months)
    if recent3months[-1] > recent12months[-1]:
        tp1 = find_next_turning_point(recent3months, recent12months, total_months - 2)
        tp2 = find_next_turning_point(recent3months, recent12months, tp1 - 1)
        all_less_than = all(v1 < v2 for v1, v2 in zip(recent3months[tp2+1:tp1], recent12months[tp2+1:tp1]))
        all_greater_than = all(v1 > v2 for v1, v2 in zip(recent3months[tp1+1:], recent12months[tp1+1:]))
        output_filename = os.path.join(dirname, '{stockname} ({stockid}).jpg'.format(**record))
        if total_months - tp1 < 5 and tp1 - tp2 > 10 and all_less_than and all_greater_than:
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
    os.remove(filename)

dog.web.quit()