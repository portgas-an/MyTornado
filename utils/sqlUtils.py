from pymysql.cursors import DictCursor


def sqlexecute(db, sql, args=None):
    cursor = db.cursor(cursor=DictCursor)
    res = cursor.execute(sql, args)
    db.commit()
    cursor.close()
    return res


def sql_Query_One(db, sql, args=None):
    cursor = db.cursor(cursor=DictCursor)
    cursor.execute(sql, args)
    res = cursor.fetchone()
    db.commit()
    cursor.close()
    return res


def sql_Query_All(db, sql, args=None):
    cursor = db.cursor(cursor=DictCursor)
    cursor.execute(sql, args)
    res = cursor.fetchall()
    db.commit()
    cursor.close()
    return res
