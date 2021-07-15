from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    flash,
    send_from_directory,
)
from models.user import User
from .utils import current_user

main = Blueprint('index', __name__)


@main.route("/")
def index():
    logged = False
    if current_user() is not None:
        logged = True
    return render_template('index.html', logged=logged, url_for=url_for)


@main.route("/register", methods=['POST'])
def register():
    u = User.register(request.form)
    if u is not None:
        register_done = '注册成功，请登录'
        flash(register_done)
        return redirect(url_for('.index'))
    else:
        register_failed = '注册失败'
        flash(register_failed)
        return redirect(url_for('.index'))


@main.route("/login", methods=['POST'])
def login():
    u = User.login(request.form)
    if u is not None:
        session['user_id'] = u.id
        logged_in = '登录成功'
        flash(logged_in)
        return redirect(url_for('.index'))
    else:
        logged_in = '登录失败'
        flash(logged_in)
        return redirect(url_for('.index'))


@main.route("/logout")
def logout():
    del session['user_id']
    return redirect(url_for('.index'))


@main.route('/static/js/<path>')
def send_js(path):
    return send_from_directory('./static/js/', path)