"""
Compute the median number of comments for each sub.
"""

import gzip
import json
from glob import glob
from collections import defaultdict

import msgpack

def main():
    ifnames = "/home/parantapa/data/reddit/reddit_post/*"
    alive_selection_name = "./alive_selection_new.txt"
    dead_selection_name = "./dead_selection_new.txt"
    comment_name = "./post_common_number.json"
    ofname = "./median_comments.json"

    with open(comment_name) as fobj:
        comment_number = dict(json.loads(x) for x in fobj)

    with open(alive_selection_name) as fobj:
        alive_selection_list = set(fobj.read().split())

    with open(dead_selection_name) as fobj:
        dead_selection_list = set(fobj.read().split())

    all_subs = alive_selection_list | dead_selection_list

    subrddit_data = defaultdict(list)
    for ifname in glob(ifnames):
        with gzip.open(ifname) as fobj:
            unpacker = msgpack.Unpacker(fobj, encoding="utf-8")
            for post in unpacker:
                id, _, sub, _, _, _, _, _, _= post
                if sub in all_subs:
                    ncomment = comment_number.get(id, 0)
                    # print 'sub=',sub, ' id= ',id
                    subrddit_data[sub].append(ncomment)

    with open(ofname,'w') as fobj:
        for sub, ncomments in subrddit_data.iteritems():
            ncomments.sort()
            mkey = len(ncomments) // 2
            median = ncomments[mkey]

            towrite = sub + " " + str(median)
            fobj.write(towrite + "\n")

if __name__ == '__main__':
    main()
