from flask import (
    render_template,
    Blueprint,
)

main = Blueprint('grammar', __name__)

@main.route("/middle_chinese")
def middle_chinese():
    return render_template('/grammar/middle_chinese.html')