import json

POSTS_LINK_FILE = './final_sub_posts.json'

POST_URL_FILE = './post_to_url.json'


with open(POST_URL_FILE) as pobj:
    post_url_dict = json.load(pobj)

# print post_url_dict
# exit()
post_link_data = {}

with open(POSTS_LINK_FILE) as pobj:
    post_link_data = json.load(pobj)


for sub,ids in post_link_data.iteritems():

    for i in ids:
        if str(i) in post_link_data.keys():
            print sub

