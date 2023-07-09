from templates.config import conn

cur = conn.cursor()

def add_user(username, email, password):
    # sql commands
    sql = f"INSERT INTO user(username, email, password) VALUES ('{username}','{email}','{password}')"
    # execute(sql)
    cur.execute(sql)
    # commit
    conn.commit()  # 对数据库内容有改变，需要commit()
    conn.close()
