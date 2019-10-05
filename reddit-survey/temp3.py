
import random


SUBREDDIT_FILE1 = 'final_subs.txt'

SUBREDDIT_FILE2 = 'final_subs2.txt'

with open(SUBREDDIT_FILE1) as obj:
    lines = []
    for line in obj.readlines():
        if len(line) == 1:
            continue
        else:
            lines.append(line)


with open(SUBREDDIT_FILE2) as fobj:
    lines2 = []
    for line in fobj.readlines():
        if len(lines) == 1:
            continue
        else:
            lines2.append(line)


lines3 = set(lines).difference(set(lines2))
# print len(lines3)

with open("final_new_sub.txt", 'w') as fobj:
    for line in lines3:
        fobj.write(line)



