import flask
import settings

# Views
from main import Main
from login import Login
from register import Register

app = flask.Flask(__name__)
app.secret_key = settings.secret_key

# Routes
app.add_url_rule('/',
                 view_func=Main.as_view('main'),
                 methods=["GET"])
app.add_url_rule('/<page>/',
                 view_func=Main.as_view('page'),
                 methods=["GET"])
app.add_url_rule('/login/',
                 view_func=Login.as_view('login'),
                 methods=["GET", "POST"])
app.add_url_rule('/register/',
                 view_func=Register.as_view('register'),
                 methods=['GET', 'POST'])

@app.errorhandler(404)
def page_not_found(error):
    return flask.render_template('404.html'), 404

app.debug = True
app.run(host='10.5.16.228',port=8888)
