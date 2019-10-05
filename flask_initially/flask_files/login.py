import flask, flask.views
import sqlite3

class Login(flask.views.MethodView):
    def get(self):
        return flask.render_template('login.html')

    def post(self):
        if 'logout' in flask.request.form:
            flask.session.pop('username', None)
            return flask.redirect(flask.url_for('login'))
        elif 'register' in flask.request.form:
            return flask.redirect(flask.url_for('register'))

        required = ['username', 'passwd']
        for r in required:
            if r not in flask.request.form:
                flask.flash("Error: {0} is required.".format(r))
                return flask.redirect(flask.url_for('login'))
        username = flask.request.form['username']
        passwd = flask.request.form['passwd']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        print passwd
        c.execute("SELECT password FROM userdata WHERE username = '%s'" % username)
        password = c.fetchone()[0]
        #flask.flash(str(password))
        if password is not None and password == passwd:
            flask.session['username'] = username
        else:

            flask.flash("Username doesn't exist or incorrect password")
        conn.close()
        return flask.redirect(flask.url_for('login'))
