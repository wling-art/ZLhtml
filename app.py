from datetime import timedelta

from flask import Flask, redirect, render_template, request, session, url_for
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import (BooleanField, EmailField, PasswordField, StringField,
                     SubmitField)
from wtforms.validators import DataRequired

from model.check_login import exist_user, is_existed
from model.check_regist import add_user

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
csrf = CSRFProtect(app)
task = None


# 使用flask的wtforms防火墙创建特殊输入框等
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    Checkbox = BooleanField('Checkbox')
    submit = SubmitField('GO~')


# 使用flask的wtforms防火墙创建特殊输入框等
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    Checkbox = BooleanField('Checkbox')
    submit = SubmitField('Join us~')


# /或者index
@app.route('/')
# index函数：作为主页的处理函数
@app.route('/index')
def index():
    return render_template('index.html')


# 作为登录界面的处理函数，主要是对于用户的登录状态进行判断，如果用户已经登录，则直接跳转到主页，否则跳转到登录界面
@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    register_form = RegisterForm()
    if request.method == 'POST':  # 注册发送
        print(
            login_form.validate_on_submit(),
            register_form.validate_on_submit(),
            request.form,
        )
        if login_form.validate_on_submit() and 'GO~' in request.form.get('submit'):
            print(
                login_form.validate_on_submit(),
                register_form.validate_on_submit(),
                request.form,
            )
        if login_form.validate_on_submit() and 'GO~' in request.form.get(  # 提交注册
            'submit'
        ):
            username = login_form.username.data
            password = login_form.password.data
            rbpwd = login_form.Checkbox.data
            if is_existed(username, password):
                session['username'] = username
                if rbpwd:
                    session.permanent = True
                # 转到页面
                return redirect(url_for('welcome'))
            if exist_user(username):
                return render_template(
                    'login.html',
                    message="密码错误!!!笨蛋!",
                    login_form=login_form,
                    register_form=register_form,
                )
            return render_template(
                'login.html',
                message="骗子！你根本不存在！",
                login_form=login_form,
                register_form=register_form,
            )

        if register_form.validate_on_submit() and 'Join us~' in request.form.get(
            'submit'
        ):
            username = register_form.username.data
            email = register_form.email.data
            password = register_form.password.data
            if exist_user(username):
                return render_template(
                    'login.html',
                    message="拜托，有人也在用这个用户名欸!",
                    login_form=login_form,
                    register_form=register_form,
                )
            add_user(username, email, password)
            return render_template(
                'login.html',
                login_form=login_form,
                register_form=register_form,
                message="你的注册很成功,可我想让你重新登录！",
            )
    return render_template(
        'login.html', login_form=login_form, register_form=register_form
    )


# 作为欢迎界面的处理函数，登录完跳转到这个页面进行欢迎，如果是没有登录跳转到这个界面则会让用户强制跳转到登录界面进行登录
@app.route('/welcome', methods=['GET'])
def welcome():
    if 'username' in session:
        return render_template('welcome.html', username=session['username'])
    return redirect(url_for('login'))


if __name__ == "__main__":
    # port8080
    app.run(host='127.0.0.1', port=5000)
