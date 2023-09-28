import os
from datetime import timedelta

from flask import Flask, redirect, render_template, request, session, url_for
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import BooleanField, EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired

from model.check_login import exist_user, is_existed
from model.change_password import is_existed as change_is_existed

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
csrf = CSRFProtect(app)


class LoginForm(FlaskForm):
    """使用flask的wtforms防火墙创建特殊输入框等"""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    Checkbox = BooleanField('Checkbox')
    submit = SubmitField('GO~')


class RegisterForm(FlaskForm):
    """使用flask的wtforms防火墙创建特殊输入框等"""

    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    Checkbox = BooleanField('Checkbox')
    submit = SubmitField('Join us~')


class ChangeForm(FlaskForm):
    """使用flask的wtforms防火墙创建特殊输入框等"""

    old_password = PasswordField(
        'old_Password',
        validators=[DataRequired()],
        id='old_password',
        render_kw={"onkeyup": "validatePassword()"},
    )
    new_password = PasswordField(
        'new_Password',
        validators=[DataRequired()],
        id='new_password',
        render_kw={"onkeyup": "validatePassword()"},
    )
    submit = SubmitField('修改', id='submit_button')


# /或者index
@app.route('/')
@app.route('/index')
def index():
    """index函数：作为主页的处理函数"""
    return render_template('index.html')


# skipcq: PY-S6007
@app.route('/login', methods=['GET', 'POST'])
def login():
    """作为登录界面的处理函数，主要是对于用户的登录状态进行判断，如果用户已经登录，则直接跳转到主页，否则跳转到登录界面"""
    login_form = LoginForm()
    # register_form = RegisterForm()
    # sourcery skip: assign-if-exp, merge-nested-ifs, reintroduce-else, swap-nested-ifs
    if request.method == 'POST' and (
        login_form.validate_on_submit() and request.form.get('submit') == 'GO~'
    ):  # 判断是否为登录
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
            )
        return render_template(
            'login.html',
            message="骗子！你根本不存在！",
            login_form=login_form,
        )
    # return render_template(
    #     'login.html', login_form=login_form, register_form=register_form
    # )
    return render_template('login.html', login_form=login_form)


@app.route('/welcome', methods=['GET'])
def welcome():
    """作为欢迎界面的处理函数，登录完跳转到这个页面进行欢迎，如果是没有登录跳转到这个界面则会让用户强制跳转到登录界面进行登录"""
    if 'username' in session:
        return render_template('welcome.html', username=session['username'])
    return redirect(url_for('login'))


@app.route('/people_info', methods=['GET', 'POST'])
def people_info():
    """作为个人信息界面的处理函数，登录完跳转到这个页面进行个人信息的查看，如果是没有登录跳转到这个界面则会让用户强制跳转到登录界面进行登录"""
    change_box = ChangeForm()
    if 'username' in session:
        if request.method == 'POST' and (
            change_box.validate_on_submit() and request.form.get('submit') == '修改'
        ):  # 判断是否为修改密码
            old_password = change_box.old_password.data
            new_password = change_box.new_password.data
            infobool, infoerror = validate_password_rules(old_password, new_password)
            if not infobool:
                return render_template(
                    'people_info.html',
                    message=infoerror,
                    username=session['username'],
                    change_box=change_box,
                )
            # 修改密码
            if change_is_existed(session['username'], new_password):
                return render_template(
                    'people_info.html',
                    message="修改成功!",
                    username=session['username'],
                    change_box=change_box,
                )
            else:
                return render_template(
                    'people_info.html',
                    message="服务器错误，修改失败!请联系管理员",
                    username=session['username'],
                    change_box=change_box,
                )

        # 如果一样就不修改
        # return render_template(
        #     'people_info.html',
        #     message="错误啦!再看看规则啊!笨蛋!",
        #     username=session['username'],
        #     change_box=change_box,
        # )
        return render_template(
            'people_info.html',
            username=session['username'],
            change_box=change_box,
        )
    return redirect(url_for('login'))


# 密码规则
def validate_password_rules(old_password, new_password):
    """判断密码是否符合规则
    ·不得与旧密码一致
    ·密码长度必须至少为5位且最多为32位
    ·至少包含3个不同的字符和1个数字

    Args:
        old_password (str(object, encoding=encoding, errors=errors)): 旧密码.
        new_password (str(object, encoding=encoding, errors=errors)): 新密码.
    """
    if old_password == new_password:
        return False, "新密码不得与旧密码一致"
    elif len(new_password) < 5 or len(new_password) > 32:
        return False, "密码长度必须至少为5位且最多为32位"
    elif len(set(new_password)) < 4:
        return False, "至少包含3个不同的字符和1个数字"
    elif not any(map(str.isdigit, new_password)):
        return False, "至少包含3个不同的字符和1个数字"
    else:
        return True, ""


if __name__ == "__main__":
    # port8080
    app.run(host='127.0.0.1', port=5000, threaded=True)
