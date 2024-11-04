import logging
import re
import random
from flask import Flask, render_template, request, session, make_response
from sqlalchemy.sql.functions import current_user
from sqlalchemy.testing.pickleable import User
from unicodedata import category
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, request, flash, redirect, url_for

from db import Database, db
from get_captcha import get_captcha_code_and_content
from functools import wraps
from flask import g, redirect
from flask import flash, url_for
from flask import Flask, session, request, make_response, jsonify


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 确保你已经设置了secret_key


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = session.get('_user_id', 0)
        user = Database().search_uid(user_id)
        if not user:
            return redirect('/login')
        g.user = user
        result = func(*args, **kwargs)
        return result
    return wrapper


@app.route('/')
@login_required
def index_view():
    user_id = session.get('_user_id', 0)
    # 查询所有数据，放到变量posts中
    posts = Database().search_blogs(user_id)
    # 把查询出来的posts传给网页
    return render_template('index.html', posts=posts)  #


@app.route('/register')
def register_view():
    return render_template('register.html')


@app.route('/login')
def login_view():
    return render_template('login.html')


@app.post('/api/register')
def register_api():
    # 1. 解析前端传递过来的数据
    data = request.get_json()
    print(data)
    # vercode = data['vercode']
    # vercode2 = session['code']
    # if vercode != vercode2:
    #     return {
    #         'message': '短信验证码错误',
    #         'code': -1
    #     }

    nickname = data['nickname']
    mobile = data['mobile']
    password = data['password']
    if not all([nickname, mobile, password]):
        return {
            'message': '数据缺失',
            'code': -1
        }
    Database().insert(nickname, mobile, password)
    return {
        'message': '注册用户成功',
        'code': 0
    }


@app.post('/api/send_register_sms')
def send_register_sms():
    # 1. 解析前端传递过来的数据
    data = request.get_json()
    mobile = data['mobile']

    # 2. 校验手机号码
    pattern = r'^1[3-9]\d{9}$'
    ret = re.match(pattern, mobile)
    if not ret:
        return {
            'message': '电话号码不符合格式',
            'code': -1
        }

    # 3. 发送短信验证码，并记录
    session['mobile'] = mobile
    # 3.1 生成随机验证码
    code = random.choices('123456789', k=6)
    session['code'] = ''.join(code)
    logging.warning(code)
    return {
        'message': '发送短信成功',
        'code': 0
    }


@app.get('/get_captcha')
def get_captcha_view():
    try:
        # 1. 获取参数
        captcha_uuid = request.args.get("captcha_uuid")
        if not captcha_uuid:
            raise ValueError("Missing 'captcha_uuid' parameter")

        # 2. 生成验证码
        code, content = get_captcha_code_and_content()

        # 3. 记录数据到会话
        session['code'] = code

        # 5. 响应返回
        resp = make_response(content)
        resp.content_type = "image/png"
        return resp
    except Exception as e:
        # 记录错误日志
        logging.error(f"Error generating captcha: {e}")
        # 清除可能已经设置的session数据
        session.pop('code', None)
        # 返回错误响应
        return jsonify({'error': 'Failed to generate captcha'}), 500


@app.post('/api/login')
def login_api():
    data = request.get_json()
    ret = Database().search(data['mobile'])
    code = session['code']
    if code != data['captcha']:
        return {
            'message': '验证码错误',
            'code': -1
        }
    if not ret:
        return {
            'message': '用户不存在',
            'code': -1
        }
    pwd = ret['password']
    if pwd != data['password']:
        return {
            'message': '用户密码错误',
            'code': -1
        }
    session['_user_id'] = ret['id']  # 记录用户登录id
    return {
        'message': '用户登录成功',
        'code': 0
    }


@app.route('/logout')
@login_required
def logout():
    session.clear()  # 清除所有session数据
    return redirect('/login')


@app.route('/posts/new', methods=('GET', 'POST'))
@login_required
def new():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        tags = request.form['tags']
        category = request.form['category']

        if not title:
            flash('标题不能为空!')
        elif not content:
            flash('内容不能为空')
        else:
            user_id = session.get('_user_id', 0)
            # 插入新内容
            print(user_id, title, content, tags, category)
            Database().insert_blog(user_id, title, content, tags, category)
            return redirect(url_for('index_view'))

    return render_template('new.html')


@app.route('/posts/<int:post_id>')
@login_required
def detail(post_id):
    detail = Database().search_bid(post_id)

    return render_template('detail.html', detail=detail)


@app.route('/posts/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = Database().search_bid(id)
    Database().delete_bid(id)
    flash('"{}" 删除成功!'.format(post['title']))
    return redirect(url_for('index_view'))


@app.route('/posts/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):
    post = Database().search_bid(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        tags = request.form['tags']
        category = request.form['category']

        if not title:
            flash('标题不能为空!')
        else:
            print(title, content, tags, category, id)
            Database().update_bid(title, content, tags, category, id)
            return redirect(url_for('index_view'))

    return render_template('edit.html', post=post)


@app.route('/about')
@login_required
def about():
    return render_template('about.html')


@app.route('/destination-plan')
@login_required
def destination_plan():
    return render_template('destination_plan.html')


@app.route('/get-weather')
@login_required
def get_weather():
    return render_template('get_weather.html')


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)
    app.run(
        app.run(debug=True)
    )
