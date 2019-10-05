"""
From all the compressed files containing posts,
this file outputs a json file with the format:
[   subreddit,
    first post time,
    last post time,
    # unique users posted,
    # posts made in this subreddit
]
"""

import gzip
import json
from glob import glob

import msgpack
import arrow

def main():
    ifnames = "/home/parantapa/data/reddit/reddit_post/*"
    ofname  = "./one.json"

    subrddit_data = {}

    for ifname in glob(ifnames):
        with gzip.open(ifname) as fobj:
            unpacker = msgpack.Unpacker(fobj, encoding="utf-8")

            for post in unpacker:
                id, author, sub, created, _, _, _, _, _= post

                if not sub in subrddit_data:
                    subrddit_data[sub] = [created, created, set([author]), 1]
                else:
                    subrddit_data[sub][0] = min(subrddit_data[sub][0], created)
                    subrddit_data[sub][1] = max(subrddit_data[sub][1], created)
                    subrddit_data[sub][2].add(author)
                    subrddit_data[sub][3] += 1

    with open(ofname, 'w') as fobj:
        for sub, (start, end, authors, nposts) in subrddit_data.iteritems():
            towrite = [sub, arrow.get(start).isoformat(),
                       arrow.get(end).isoformat(),
                       len(authors), nposts]
            fobj.write(json.dumps(towrite) + "\n")

if __name__ == '__main__':
    main()
