import os, shutil, statementdog

# login
dog = statementdog.statementdog().login()

# make output directory
dirname = 'monthly-revenue-yoy-turning'
if os.path.exists(dirname):
    shutil.rmtree(dirname)
os.mkdir(dirname)

def find_next_turning_point(curv1, curv2, start_point):
    while start_point >= 0:
        if (curv1[start_point] - curv2[start_point]) * (curv1[start_point+1] - curv2[start_point+1]) < 0:
            return start_point
        else:
            start_point -= 1
    return start_point

records = dog.select_stock('近三月營收年增率3個月內漲破近6月')
print('len(records) = ', len(records))
for i, record in enumerate(records):
    print(f'goto {record["stockid"]}({i}/{len(records)})')
    [recent3months, _, recent12months] = dog.goto(record['stockid']).get_data_table()
    total_months = len(recent3months)
    if recent3months[-1] > recent12months[-1]:
        tp1 = find_next_turning_point(recent3months, recent12months, total_months - 2)
        tp2 = find_next_turning_point(recent3months, recent12months, tp1 - 1)
        all_greater_than = all(v1 > v2 for v1, v2 in zip(recent3months[tp1+1:], recent12months[tp1+1:]))
        output_filename = os.path.join(dirname, '{stockname} ({stockid}).jpg'.format(**record))
        # if total_months - tp1 < 5 and tp1 - tp2 > 10:
        if total_months - tp1 < 5 and all_greater_than:
            dog.capture_monthly_revenue_yoy(record['stockid'], output_filename)
            print('added {stockname} ({stockid})'.format(**record))

dog.web.quit()