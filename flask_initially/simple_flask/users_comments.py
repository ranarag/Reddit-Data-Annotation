import flask, flask.views
import sqlite3
app = flask.Flask(__name__)
app.config.from_envvar('config.cfg',silent=True)
conn = None
c = None
@app.before_request
def before_request():
    global conn
    global c
    conn = sqlite3.connect(app.config['DATABASE'])
    c = conn.cursor()


@app.teardown_request
def teardown_request(exception):
    global conn

    conn.commit()
    conn.close()




class Comment_storer(flask.views.MethodView):
    def get(self):
        return flask.render_template('reg.html')
    def post(self):

        fields = ['username',"comment"]
        for f in fields:
            if f not in flask.request.form:
                # print "field"+f+"not present"
                return flask.render_template('reg.html')

        comm = flask.request.form['comment']

        userN = flask.request.form['username']

        c.execute('INSERT INTO usercomments VALUES(?,?)',(userN
            ,comm))
        return self.get()




app.add_url_rule('/',
                 view_func=Comment_storer.as_view('main'),
                 methods=["GET","POST"])
app.debug = True
app.run()
