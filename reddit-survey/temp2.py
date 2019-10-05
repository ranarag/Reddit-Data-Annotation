import json

POST_TITLE_FILE = './post_to_title.json'
with open(POST_TITLE_FILE) as pobj:
    post_to_title = json.load(pobj)

print "done2"

post_idlist = []
for ids,_ in post_to_title.iteritems():
    post_idlist.append(ids)

post_idlist = set(post_idlist)
post_to_title.clear()

print "done1"


comm = {}
file1 = open('post_common_number.json','r')
for data in file1:
    i = json.loads(data)
    if str(i[0]) in post_idlist:
        comm[i[0]] = i[1]
print "done3"
with open("comment_counts.json",'w') as fobj:
    json.dump(comm,fobj)
