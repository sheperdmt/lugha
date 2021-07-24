from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    flash,
)
from models.user import User
from .utils import current_user

main = Blueprint('index', __name__)

REGISTER_DONE = '注册成功，请登录'
REGISTER_FAILED = '注册失败'
LOGGED_IN = '登录成功'
NOT_LOGGED_IN = '登录失败'

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
        flash(REGISTER_DONE)
        return redirect(url_for('.index'))
    else:
        flash(REGISTER_FAILED)
        return redirect(url_for('.index'))


@main.route("/login", methods=['GET', 'POST'])
def login():
    u = User.login(request.form)
    if u is not None:
        session['user_id'] = u.id
        flash(LOGGED_IN)
        return redirect(url_for('.index'))
    else:
        flash(NOT_LOGGED_IN)
        return redirect(url_for('.index'))


@main.route("/logout")
def logout():
    del session['user_id']
    return redirect(url_for('.index'))