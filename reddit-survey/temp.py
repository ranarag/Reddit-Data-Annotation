import sqlite3
# import flask
conn = sqlite3.connect("data.sqlite3")

c = conn.cursor()

# c.execute('''CREATE TABLE usercomments
             # (name text, comment text)''')

c.execute('SELECT * FROM survey')
print len(c.fetchall())
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
