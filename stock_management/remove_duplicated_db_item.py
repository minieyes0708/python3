from DBController import DBController

with DBController() as db:
    duplicate_items = db.fetchall('''
    SELECT CONCAT(`date_info`, ',', `stock_id`) AS uniq FROM `everyday_close_info`
    GROUP BY uniq
    HAVING COUNT(uniq) > 1
    ''')
    duplicate_items = [item['uniq'] for item in duplicate_items]
    for duplicate_item in duplicate_items:
        date_info, stock_id = duplicate_item.split(',')
        db_items = db.fetchall('''
        SELECT `record_index` FROM `everyday_close_info`
        WHERE `date_info` = '{date_info}' AND `stock_id` = '{stock_id}'
        '''.format(**{
            'date_info': date_info,
            'stock_id': stock_id
        }))
        for index in range(len(db_items) - 1):
            db.execute('''
            DELETE FROM `everyday_close_info` WHERE `record_index` = {record_index}
            '''.format(**{
                'record_index': db_items[index]['record_index']
            }))
            db.commit()
