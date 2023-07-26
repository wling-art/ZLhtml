from flask import Flask, jsonify, request, make_response, redirect
import requests

app = Flask(__name__)


# 定义 Flask 登录页面的路由
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method != 'POST':
        return '''
        <form method="post" action="/login">
            <input type="text" name="username" placeholder="用户名">
            <input type="password" name="password" placeholder="密码">
            <input type="submit" value="登录">
        </form>
    '''
    print(request.form)
    # 获取用户提交的登录信息
    username = request.form.get('username')
    password = request.form.get('password')

    # 构建登录请求参数
    login_data = {'j_username': username, 'j_password': password, 'login': 'Login'}

    # 使用 requests 库将登录信息发送给 up/login.php

    php_login_url = 'http://192.168.10.39:8123/up/login'  # 假设 up/login.php 的 URL
    response = requests.post(php_login_url, data=login_data)

    # 获取 up/login.php 返回的结果
    result = response.json()
    print(result)

    if result['result'] != 'success':
        # 登录失败，直接返回 JSON 响应给用户
        return jsonify(result)
    # 登录失败，直接返回 JSON 响应给用户
    # 登录成功，设置 PHP Session 中的 userid 作为 Cookie
    userid = username  # 假设登录成功后的用户名在 'userid' 字段中
    php_cookie = response.cookies.get_dict()
    php_cookie['PHPSESSID'] = userid  # 假设 PHP Session 的 Cookie 名称是 PHPSESSID
    # 创建 Flask 响应对象，将登录成功的 JSON 响应和 Cookie 返回给用户
    flask_response = make_response(jsonify(result))
    for key, value in php_cookie.items():
        flask_response.set_cookie(key, value)
    # 登录成功后重定向到 http://192.168.10.39:8123/index.html
    return redirect('http://192.168.10.39:8123/index.html', code=302)


if __name__ == '__main__':
    app.run(debug=True)
