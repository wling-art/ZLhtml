from templates.config import conn

cur = conn.cursor()


def is_null(username, password):
    return username == '' or password == ''


def is_existed(username, password):  # 注册时检查用户名是否存在
    sql = "SELECT * FROM user WHERE username = %s and password = %s"
    conn.ping(reconnect=True)
    cur.execute(sql, (username, password))
    result = cur.fetchall()
    conn.close()
    return len(result) != 0


def exist_user(username):  # 注册时检查用户名是否存在
    sql = "SELECT * FROM user WHERE username = %s"
    conn.ping(reconnect=True)
    cur.execute(sql, (username,))
    result = cur.fetchall()
    conn.close()
    return len(result) != 0
