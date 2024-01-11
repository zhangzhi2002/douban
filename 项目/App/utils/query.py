from pymysql import *

coon = connect(host='localhost', port=3306, user='root', passwd='123456', db='豆瓣')
cursor = coon.cursor()


def querys(sql, params, type='no_select'):
    params = tuple(params)
    cursor.execute(sql, params)
    if type != 'no_select':
        data_list=cursor.fetchall()
        coon.commit()
        return data_list
    else:
        coon.commit()
        return "数据库语句执行成功"