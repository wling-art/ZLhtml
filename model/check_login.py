from model.config import conn
from hashlib import sha512

cur = conn.cursor()


def is_null(username, password):
    """判断用户名和密码是否为空"""
    return username == '' or password == ''


def is_existed(username, password):  # 注册时检查用户名是否存在
    """判断用户名和密码是否存在"""
    # 进行加密
    password_sha512 = sha512(password.encode('utf-8')).hexdigest()
    sql = "SELECT * FROM nexauth_users WHERE name = %s and password = %s"
    conn.ping(reconnect=True)
    cur.execute(sql, (username, password_sha512))
    result = cur.fetchall()
    conn.close()
    return len(result) != 0


def exist_user(username):  # 注册时检查用户名是否存在
    """判断用户名是否存在"""
    sql = "SELECT * FROM nexauth_users WHERE name = %s"
    conn.ping(reconnect=True)
    cur.execute(sql, (username,))
    result = cur.fetchall()
    conn.close()
    return len(result) != 0
