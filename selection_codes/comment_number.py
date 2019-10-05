"""
Write the #comments to every post
"""

import gzip
import json
from glob import glob

import msgpack

def main():
    ifnames = "/home/parantapa/data/reddit/reddit_comment/*"
    ofname = "./post_common_number.json"

    comment_linkid_data = {}
    for ifname in glob(ifnames):
        with gzip.open(ifname) as fobj:
            unpacker = msgpack.Unpacker(fobj, encoding="utf-8")
            for comment in unpacker:
                _, _, _, _, link_id, _, _, _, _,_ = comment

                if not link_id in comment_linkid_data:
                    comment_linkid_data[link_id] = 1
                else:
                    comment_linkid_data[link_id] += 1

    with open(ofname, 'w') as fobj:
        for link_id, ncomments in comment_linkid_data.iteritems():
            towrite = [link_id, ncomments]
            fobj.write(json.dumps(towrite) + "\n")

if __name__ == '__main__':
    main()
