# from datetime import timedelta
# import os
# from flask import Flask, render_template, jsonify, request, make_response, redirect
# from flask import redirect
# from flask import session
# from flask import url_for
# from flask import request
# from model.check_login import is_existed, exist_user, is_null
# from model.check_regist import add_user
# from flask_wtf.csrf import CSRFProtect
# from flask_wtf import FlaskForm
# from wtforms import (
#     StringField,
#     PasswordField,
#     SubmitField,
#     EmailField,
#     BooleanField,
#     Form,
# )
# import requests
# from wtforms.validators import DataRequired

# app = Flask(__name__, static_folder='static', template_folder='templates')
# app.secret_key = os.urandom(24)
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
# csrf = CSRFProtect(app)
# task = None


# class LoginForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     cheackbox = BooleanField('Cheackbox')
#     submit = SubmitField('GO~')


# class RegisterForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired()])
#     email = EmailField('Email', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     cheackbox = BooleanField('cheackbox')
#     submit = SubmitField('Join us~')


# # /或者index
# @app.route('/')
# @app.route('/index')
# def index():
#     return render_template('index.html')


# @app.route('/login', methods=['GET', 'POST'])
# def user_login():
#     login_form = LoginForm()
#     register_form = RegisterForm()
#     if request.method == 'POST':  # 注册发送
#         print(
#             login_form.validate_on_submit(),
#             register_form.validate_on_submit(),
#             request.form,
#         )
#         if login_form.validate_on_submit() and 'GO~' in request.form.get('submit'):
#             print(
#                 login_form.validate_on_submit(),
#                 register_form.validate_on_submit(),
#                 request.form,
#             )
#         if login_form.validate_on_submit() and 'GO~' in request.form.get(  # 提交注册
#             'submit'
#         ):
#             username = login_form.username.data
#             password = login_form.password.data
#             rbpwd = login_form.cheackbox.data
#             if is_existed(username, password):
#                 session['username'] = username
#                 if rbpwd:
#                     session.permanent = True
#                 # 转到页面
#                 return redirect(url_for('index'))
#             elif exist_user(username):
#                 return render_template(
#                     'login.html',
#                     message="密码错误!!!笨蛋!",
#                     login_form=login_form,
#                     register_form=register_form,
#                 )
#             else:
#                 return render_template(
#                     'login.html',
#                     message="骗子！你根本不存在！",
#                     login_form=login_form,
#                     register_form=register_form,
#                 )

#         if register_form.validate_on_submit() and 'Join us~' in request.form.get(
#             'submit'
#         ):
#             username = register_form.username.data
#             email = register_form.email.data
#             password = register_form.password.data
#             if exist_user(username):
#                 return render_template(
#                     'login.html',
#                     message="拜托，有人也在用这个用户名欸!",
#                     login_form=login_form,
#                     register_form=register_form,
#                 )
#             add_user(username, email, password)
#             return render_template(
#                 'login.html',
#                 login_form=login_form,
#                 register_form=register_form,
#                 message="你的注册很成功,可我想让你重新登录！",
#             )
#     return render_template(
#         'login.html', login_form=login_form, register_form=register_form
#     )

from flask import Flask, jsonify, request, make_response, redirect
import requests

app = Flask(__name__)


@app.route('/login_flask', methods=['POST', 'GET'])
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

    php_login_url = 'http://49.232.240.247:8123/up/login'  # 假设 up/login.php 的 URL
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
    return redirect('http://49.232.240.247/:8123/index.html', code=302)


if __name__ == "__main__":
    # port8080
    app.run(host='0.0.0.0', port=5000)
