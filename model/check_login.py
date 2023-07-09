from templates.config import conn

cur = conn.cursor()


def is_null(username, password):
    return username == '' or password == ''


def is_existed(username, password):  #注册时检查用户名是否存在
    sql = f"SELECT * FROM user WHERE username ='{username}' and password ='{password}'"
    cur.execute(sql)
    result = cur.fetchall()
    return len(result) != 0


def exist_user(username):  #注册时检查用户名是否存在
    sql = f"SELECT * FROM user WHERE username ='{username}'"
    cur.execute(sql)
    result = cur.fetchall()
    return len(result) != 0
