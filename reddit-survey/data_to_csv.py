import pandas as pd
import json
from numpy import base_repr
import sqlite3

conn = sqlite3.connect('data.sqlite3')

cur = conn.cursor()

POST_URL_FILE = './post_to_url.json'

POST_TITLE_FILE = './post_to_title.json'

POSTS_LINK_FILE = './final_sub_posts.json'

POST_AUTHOR_DATE_FILE = './post_to_author_and_date.json'

POST_COMMENTS_FILE = './comment_counts.json'

SUBREDDIT_FILE = "./final_subs2.txt"

output_file = 'diff_labels2.txt'

with open(POST_URL_FILE) as pobj:
    post_url_dict = json.load(pobj)

with open(POST_TITLE_FILE) as pobj:
    post_to_title = json.load(pobj)


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

# subreddit = {}
posts = {}
for sub in lines:
    # posts = []
    for i in post_link_data[sub]:
        post = {}
        res = {}
        num = base_repr(int(i), 36)
        cur.execute("select * from psurvey where pid = ? and user = ?",
            [str(num), "Anurag"])

        res['Anurag'] = cur.fetchone()[2]
        cur.execute("select * from psurvey where pid = ? and user = ?",
            [str(num), "Ratndeep"])

        res['Ratnadeep'] = cur.fetchone()[2]

        # exit()
        # post['id'] = i
        post['subreddit'] = sub
        link = "https://reddit.com/r/"+sub+"/comments/"+num
        post['author'] = post_author_date[str(i)]['author']
        post['date'] = post_author_date[str(i)]['posted_on']
        post['title'] = post_to_title[str(i)]
        try:
            post['n_comments'] = post_to_comments[str(i)]
        except:
            post['n_comments'] = 0
        try:
            post['post_url'] = post_url_dict[str(i)][0]

        except:
            post['post_url'] = link

        post['comment'] = link
        post['response'] = res
        if res['Anurag'] * res['Ratnadeep'] < 0:
            with open(output_file, 'a') as fid:
                fid.write(str(res) + "," + str(i)+'\n')
        posts[i] = post


    # subreddit[sub] = l

# print posts

# print subreddit.keys()
df = pd.DataFrame.from_dict(posts, orient='index')
# df.columns = ['sub_link', 'post_0', 'post_1', 'post_2', 'post_3', 'post_4',
#                 'post_5', 'post_6', 'post_7', 'post_8', 'post_9' ]
df.index.name = 'post_id'
print df.head()
# exit()
df.to_csv("subreddit_data2.csv", encoding='utf-8')

