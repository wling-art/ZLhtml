from datetime import timedelta
import os
from flask import Flask, render_template
from flask import redirect
from flask import session
from flask import url_for
from flask import request
from model.check_login import is_existed, exist_user, is_null
from model.check_regist import add_user
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
# checkbox
from wtforms import StringField, PasswordField, SubmitField, EmailField, BooleanField, Form
from wtforms.validators import DataRequired

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
csrf = CSRFProtect(app)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    cheackbox = BooleanField('Cheackbox')
    submit = SubmitField('GO~')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    cheackbox = BooleanField('cheackbox')
    submit = SubmitField('Join us~')


# /或者index
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
    # return redirect(url_for('user_login'))


@app.route('/login', methods=['GET', 'POST'])
def user_login():
    login_form = LoginForm()
    register_form = RegisterForm()
    if request.method == 'POST':  # 注册发送
        print(login_form.validate_on_submit(),
              register_form.validate_on_submit(), request.form)
        if login_form.validate_on_submit() and 'GO~' in request.form.get(
                'submit'):
            username = login_form.username.data
            password = login_form.password.data
            rbpwd = login_form.cheackbox.data
            if is_existed(username, password):
                session['username'] = username
                if rbpwd:
                    session.permanent = True
                # 转到页面
                return redirect(url_for('index'))
            elif exist_user(username):
                return render_template('login.html',
                                       message="密码错误!!!笨蛋!",
                                       login_form=login_form,
                                       register_form=register_form)
            else:
                return render_template('login.html',
                                       message="骗子！你根本不存在！",
                                       login_form=login_form,
                                       register_form=register_form)

        if register_form.validate_on_submit(
        ) and 'Join us~' in request.form.get('submit'):
            username = register_form.username.data
            email = register_form.email.data
            password = register_form.password.data
            if exist_user(username):
                return render_template('login.html',
                                       message="拜托，有人也在用这个用户名欸!",
                                       login_form=login_form,
                                       register_form=register_form)
            add_user(username, email, password)
            return render_template('login.html',
                                   login_form=login_form,
                                   register_form=register_form,
                                   message="你的注册很成功,可我想让你重新登陆！")
    return render_template('login.html',
                           login_form=login_form,
                           register_form=register_form)


if __name__ == "__main__":
    # port8080
    app.run(host='0.0.0.0', port=8080)
    app.run()
