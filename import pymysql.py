import pymysql
from flask import Flask
from flask import g

app = Flask(__name__)

# MySQL数据库连接配置
DATABASE = {
    'host': '192.168.10.39',
    'user': 'zlhtml',
    'password': 'cMdXkMfA5s7ipzxj',
    'database': 'zlhtml',
}


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = pymysql.connect(
            host=DATABASE['host'],
            user=DATABASE['user'],
            password=DATABASE['password'],
            database=DATABASE['database']
        )
    return db


def create_table():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);
''')
    db.commit()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    with app.app_context():
        create_table()
        app.run(host='0.0.0.0', port=8080)
