from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    flash,
)

main = Blueprint('user', __name__)


@main.route('/index')
def index():
    return ''