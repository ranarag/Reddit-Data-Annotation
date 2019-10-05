"""
Outputs random posts which have greater than
    median comments for all selected subreddits.
"""

import gzip
import json
import random
from glob import glob
from collections import defaultdict

import msgpack

def main():

    ifnames = "/home/parantapa/data/reddit/reddit_post/*"
    median_name = './median_comments.txt'
    comment_name = "./post_common_number.json"
    ofname = "./final_sub_posts.json"

    median_data = {}
    with open(median_name) as fobj:
        for line in fobj:
            if len(line) > 1:
                cols = line.split()
                median_data[cols[0]] = int(cols[1])

    comment_number = {}
    with open(comment_name) as fobj:
        for line in fobj:
            line = json.loads(line)
            comment_number[line[0]] = int(line[1])

    subrddit_data = defaultdict(list)
    for ifname in glob(ifnames):
        with gzip.open(ifname) as fobj:
            unpacker = msgpack.Unpacker(fobj, encoding="utf-8")
            for post in unpacker:
                id, _, sub, _, _, _, _, _, _ = post

                if sub in median_data:
                    ncoms = comment_number.get(id, 0)
                    # print 'sub=',sub, ' id= ',id
                    if ncoms >= median_data[sub]:
                        subrddit_data[sub].append(id)

    for sub, link_ids in subrddit_data.iteritems():
        if len(link_ids) > 10:
            link_ids = random.sample(link_ids, 10)
        subrddit_data[sub] = link_ids

    with open(ofname, 'w') as fobj:
        json.dump(subrddit_data, fobj)

if __name__ == '__main__':
    main()

