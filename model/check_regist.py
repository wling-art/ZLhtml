from model.config import conn

cur = conn.cursor()


def add_user(username, email, password):
    """注册时添加用户"""
    # sql commands
    sql = "INSERT INTO nexauth_users(name, email, password) VALUES (%s, %s, %s)"
    values = (username, email, password)
    conn.ping(reconnect=True)
    # execute(sql)
    cur.execute(sql, values)
    # commit
    conn.commit()  # 对数据库内容有改变，需要commit()
    conn.close()
