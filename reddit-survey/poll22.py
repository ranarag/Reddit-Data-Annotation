#!/usr/bin/env python
""" This script prompts a user to enter a message to encode or decode
using a classic Caeser shift substitution (3 letter shift) """


import time
import sqlite3
import json
from flask import Flask, render_template, request
from flask import g, url_for
from contextlib import closing
from numpy import base_repr
import flask


app = Flask(__name__)
app.secret_key = "asadad"
DATABASE = "./data.sqlite3"

SUBREDDIT_FILE = "./final_subs2.txt"

JSONFILE = './user-reddit.json'

POSTS_LINK_FILE = './final_sub_posts.json'

POST_URL_FILE = './post_to_url.json'

POST_AUTHOR_DATE_FILE = './post_to_author_and_date.json'

POST_TITLE_FILE = './post_to_title.json'

POST_COMMENTS_FILE = './comment_counts.json'

DEFAULT_PARAMS = {
    "survey": {
        "title": "Identifying sources of value for subreddits",
        "description": (
            "Survey on categorizing post-based/comment-based subreddits"
            "in Reddit."),
    }
}

with open(POST_COMMENTS_FILE) as pobj:
    post_to_comments = json.load(pobj)

with open(POST_TITLE_FILE) as pobj:
    post_to_title = json.load(pobj)


with open(POST_AUTHOR_DATE_FILE) as pobj:
    post_author_date = json.load(pobj)

with open(POST_URL_FILE) as pobj:
    post_url_dict = json.load(pobj)

# print post_url_dict
# exit()
post_link_data = {}

with open(POSTS_LINK_FILE) as pobj:
    post_link_data = json.load(pobj)


with open(SUBREDDIT_FILE) as obj:
    lines = []
    for line in obj.readlines():
        if len(line) == 1:
            continue
        else:
            line = line[:-1]
            lines.append(line)


with open(JSONFILE) as jf:
    key_data = json.load(jf)


def connect_db():
    return sqlite3.connect(DATABASE)


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as fobj:
            db.cursor().executescript(fobj.read())
        db.commit()

def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    g.db.commit()
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


@app.before_request
def before_request():
    g.db = connect_db()


@app.after_request
def after_request(response):
    g.db.commit()
    g.db.close()
    return response

# Initial program for execution


@app.route('/')
def root():
    params = dict(DEFAULT_PARAMS)
    params.update({
        "next_page": url_for("survey_begin")
    })
    return render_template('instructions.html.jinja2', **params)


@app.route('/url')
def url_root():
    params = dict(DEFAULT_PARAMS)
    key = request.args.get('c')

    params.update({
        "next_page": url_for("survey_begin", c=key),
        "participant": key_data[key]['participant'],
        "npages": key_data[key]['npages']
    })

    return render_template('instructions.html.jinja2', **params)

"""for beginning survey ---- starts after root execution """


@app.route('/start_survey')
def survey_begin():
    # global params
    global key_data
    c = request.args.get('c')
    # key = c
    # c = "wizxhk2oeo"
    params = dict(DEFAULT_PARAMS)
    sub = lines[key_data[c]['index']]
    posts = []
    for i in post_link_data[sub]:
        post = {}

        num = base_repr(int(i), 36)
        post['id'] = num
        link = "https://reddit.com/r/"+sub+"/comments/"+num
        post['author'] = post_author_date[str(i)]['author']
        post['date'] = post_author_date[str(i)]['posted_on']
        post['title'] = post_to_title[str(i)]
        try:
            post['n_comments'] = post_to_comments[str(i)]
        except:
            post['n_comments'] = 0
        try:
            post['url'] = post_url_dict[str(i)][0]

        except:
            post['url'] = link

        post['comment'] = link
        posts.append(post)
        subreddit = {}
        subreddit['name'] = lines[key_data[c]['index']]
        subreddit['id'] = key_data[c]['index']
    params.update({
        "c": c,
        "subreddit": subreddit,
        "nmore": key_data[c]['npages'],
        "progress_percent": 0,
        "posts": posts
        })
    # prev_n = len(post_links)
    return render_template('poll2.html.jinja2', **params)


""" for polling ---- starts after survey begin """


@app.route('/poll/<int:id>', methods=["GET", "POST"])
def poll(id):
    print "IN poll"
    # global params
    global key_data
    params = dict(DEFAULT_PARAMS)
    key = request.args.get('c')
    # posts = params['posts']

    for rquest in flask.request.form.keys():
        if rquest == 'c':
            continue
        elif "post_response" in rquest:
            result = flask.request.form[rquest].split(',')

            vote = int(result[1])
            g.db.execute("insert into psurvey values(?,?,?,?)", [result[0],
                    key_data[key]['participant'],
                    vote,
                    time.ctime()])

    if id+1 >= key_data[key]['npages'] + key_data[key]['index']:

        params.update({"participant": key_data[key]['participant']})

        return render_template('finish.html.jinja2', **params)
    else:

        sub = lines[id+1]
        posts = []
        for i in post_link_data[sub]:
            post = {}

            num = base_repr(int(i), 36)
            post['id'] = num
            link = "https://reddit.com/r/"+sub+"/comments/"+num
            post['author'] = post_author_date[str(i)]['author']
            post['date'] = post_author_date[str(i)]['posted_on']
            post['title'] = post_to_title[str(i)]
            try:
                post['n_comments'] = post_to_comments[str(i)]
            except:
                post['n_comments'] = 0
            try:
                post['url'] = post_url_dict[str(i)][0]

            except:
                post['url'] = link

            post['comment'] = link
            posts.append(post)
            subreddit = {}
            subreddit['name'] = lines[id+1]
            subreddit['id'] = id + 1

        params.update({
            "c": key,
            "subreddit": subreddit,
            "nmore": key_data[key]['npages']-(id-key_data[key]['index']+1),
            "progress_percent": float(id-key_data[key]['index'] + 1) /
            key_data[key]['npages']*100,
            "posts": posts

            })
        return render_template('poll2.html.jinja2', **params)



@app.route('/result/<int:id>', methods=["GET"])
def result(id):
    print "IN poll"
    # global params
    global key_data
    params = dict(DEFAULT_PARAMS)
    key = request.args.get('c')
    # posts = params['posts']

    if id+1 >= key_data[key]['npages'] + key_data[key]['index']:

        params.update({"participant": key_data[key]['participant']})

        return render_template('finish.html.jinja2', **params)
    else:

        sub = lines[id+1]
        posts = []
        reSults = {}
        for i in post_link_data[sub]:
            post = {}

            num = base_repr(int(i), 36)
            post['id'] = num

            res = query_db("select * from psurvey where pid = ? and user = ?",[str(num), str(key_data[key]['participant'])], True)
            reSults[str(num)] = res

            link = "https://reddit.com/r/"+sub+"/comments/"+num
            post['author'] = post_author_date[str(i)]['author']
            post['date'] = post_author_date[str(i)]['posted_on']
            post['title'] = post_to_title[str(i)]
            try:
                post['n_comments'] = post_to_comments[str(i)]
            except:
                post['n_comments'] = 0
            try:
                post['url'] = post_url_dict[str(i)][0]

            except:
                post['url'] = link

            post['comment'] = link
            posts.append(post)
            subreddit = {}
            subreddit['name'] = lines[id+1]
            subreddit['id'] = id + 1

        params.update({
            "c": key,
            "subreddit": subreddit,
            "nmore": key_data[key]['npages']-(id-key_data[key]['index']+1),
            "progress_percent": float(id-key_data[key]['index'] + 1) /
            key_data[key]['npages']*100,
            "posts": posts,
            "results": reSults

            })
        return render_template('view_results.html.jinja2', **params)


if  __name__  ==  '__main__':
    app.run(debug=True)
