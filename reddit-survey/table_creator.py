import sqlite3
# import flask
conn = sqlite3.connect("data.sqlite3")

c = conn.cursor()

# c.execute('''CREATE TABLE usercomments
             # (name text, comment text)''')
# create table user(
#    roll text primary key,
#    name text);
#  create table survey(
#    user text,
#    subreddit text,
#    value integer);

c.execute('create table psurvey(pid text,user text,value integer,subtime text);')
# c.execute('create table subsurvey(subreddit text,user text,value integer,subtime text);')
# c.execute("select * from subsurvey")
# print c.fetchall()
# conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
