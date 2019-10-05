import sqlite3
import flask
app = flask.Flask(__name__)
app.config.from_envvar('/config.cfg', silent=True)
for i in app.config.iteritems():
    print i
app.run()
conn = sqlite3.connect(app.config['DATABASE'])

c = conn.cursor()

c.execute('''CREATE TABLE usercomments
             (name text, comment text)''')

# c.execute('SELECT * FROM usercomments')
# print c.fetchone()
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
