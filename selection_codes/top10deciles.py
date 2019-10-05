"""
Output alive_selection.txt and dead_selection.txt where
alive_selection.txt contains all alive subreddits
    that have minimunm 10 unique users
and are not first 100 subreddits or 100 default subreddits
"""

import json
import random

def main():
    ifname = "./one.json"

    defsubsname = './default-subs-1Jan14.txt'
    first100subname = './first100-subs.txt'
    deadname = "./deadsubs.txt"
    alivename = "./alivesubs.txt"

    alive_selection_name = './alive_selection.txt'
    dead_selection_name = './dead_selection.txt'

    with open(alivename) as fobj:
        alivesubs = set(sub.split()[0] for sub in fobj)
    with open(deadname) as fobj:
        deadsubs = set(sub.split()[0] for sub in fobj)
    with open(defsubsname) as fobj:
        defsubs = set(sub.split()[0] for sub in fobj)
    with open(first100subname) as fobj:
        first100subs = set(sub.split()[-1] for sub in fobj)

    sublist = []
    with open(ifname) as fobj:
        for line in fobj:
            line = json.loads(line)

            # only consider subreddits with more than 10 unique users
            if int(line[3]) >= 10:
                sublist.append(line)
    sublist.sort(key=lambda row: -row[3])
    sublist = [sub[0] for sub in sublist]

    size = len(sublist) / 10

    with open(alive_selection_name, 'w') as afobj:
        with open(dead_selection_name, 'w') as dfobj:
            for i in range(10):
                base_set = sublist[i * size : (i + 1) * size]
                base_set = set(base_set) - first100subs - defsubs

                alive_selection = list(alivesubs & base_set)
                dead_selection = list(deadsubs & base_set)

                alive_selection = random.sample(alive_selection, 30)
                dead_selection = random.sample(dead_selection, 30)

                for sub in alive_selection:
                    afobj.write(sub + "\n")
                afobj.write('\n')

                for sub in dead_selection:
                    dfobj.write(sub + "\n")
                dfobj.write('\n')

if __name__ == '__main__':
    main()
