import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()

# c.execute('''CREATE TABLE userdata
#              (name text, number integer, username text, password text)''')

c.execute('SELECT * FROM userdata')
print c.fetchone()
# conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
