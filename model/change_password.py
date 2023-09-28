import bcrypt

from model.config import conn

cur = conn.cursor()


def is_existed(username, password):
    """修改密码

    Args:
        username (str(object, encoding=encoding, errors=errors)): 修改时需要的用户名
        password (str(object, encoding=encoding, errors=errors)): 需要修改的密码
    """
    # 进行加密
    password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    # 获取该用户名的密码
    sql = "UPDATE nexauth_users SET password = %s WHERE name = %s"
    conn.ping(reconnect=True)
    cur.execute(sql, (password, username))
    conn.commit()
    conn.close()
    return True
