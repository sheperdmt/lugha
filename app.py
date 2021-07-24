from flask import Flask

import config

app = Flask(
    __name__,
    )
app.secret_key = config.secret_key


from routes import main as index_routes
from routes.word import main as word_routes
from routes.api import main as api_routes
from routes.user import main as user_routes
from routes.utils import current_user

app.register_blueprint(index_routes)
app.register_blueprint(word_routes, url_prefix='/word')
app.register_blueprint(api_routes, url_prefix='/api')
app.register_blueprint(user_routes, url_prefix='/user')

    
@app.context_processor
def inject_user():
    user = current_user()
    return dict(user=user)


if __name__ == '__main__':
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=2000,
    )
    app.run(**config)

