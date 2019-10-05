import flask, flask.views
import sqlite3



class Register(flask.views.MethodView):
    def get(self):
        return flask.render_template('register.html')

    def post(self):
        fields = ['name','contact_no','username','passwd']
        for f in fields:
            if f not in flask.request.form:
                print "You forgot to enter" + f
                return flask.redirect(flask.url_for('register'))
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT username from userdata")
        users = c.fetchone()
        if users is not None and flask.request.form['username'] in users:
            print "It seems that you are already registered :P"
            return flask.redirect(flask.url_for('login'))
        name = flask.request.form['name']
        number = flask.request.form['contact_no']
        usrname = flask.request.form['username']
        password = str(flask.request.form['passwd'])

        c.execute("INSERT INTO userdata VALUES (?,?,?,?)",(name,number,usrname,password))
        conn.commit()
        conn.close()
        return flask.redirect(flask.url_for('login'))
