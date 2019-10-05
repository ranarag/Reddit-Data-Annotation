"""
The end of dataset
"""

import json

import arrow

def main():
    ifname = "./one.json"

    with open(ifname) as fobj:
        lastpost = -1
        for line in fobj:
            line = json.loads(line)
            t = arrow.get(line[2]).timestamp
            lastpost = max(lastpost, t)

        print lastpost, arrow.get(lastpost)
        # "Result - 1441065599 2015-08-31T23:59:59+00:00"

if __name__ == '__main__':
    main()

