import bcrypt

from model.config import conn

cur = conn.cursor()


def is_null(username, password):
    """判断用户名和密码是否为空"""
    return username == '' or password == ''


def is_existed(username, password):  # 注册时检查用户名是否存在
    """判断用户名和密码是否存在"""
    # 获取该用户名的密码
    sql = "SELECT password FROM nexauth_users WHERE name = %s"
    conn.ping(reconnect=True)
    cur.execute(sql, (username,))
    result = cur.fetchall()
    conn.close()
    # 进行BCrypt验证
    return bcrypt.checkpw(password.encode('utf-8'), result[0][0].encode('utf-8'))


def exist_user(username):  # 注册时检查用户名是否存在
    """判断用户名是否存在"""
    sql = "SELECT * FROM nexauth_users WHERE name = %s"
    conn.ping(reconnect=True)
    cur.execute(sql, (username,))
    result = cur.fetchall()
    conn.close()
    return len(result) != 0
