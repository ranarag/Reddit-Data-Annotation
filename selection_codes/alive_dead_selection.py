"""
Output alive subreddits and dead subreddits.
"""

import json

import arrow

def main():
    ifname = "./one.json"
    deadname = "./deadsubs.txt"
    alivename = "./alivesubs.txt"

    endtime = 1441065599 # end of dataset time

    ONE_MONTH = 30 * 24 * 60 * 60
    SIX_MONTHS = 6 * ONE_MONTH
    SEVEN_MONTHS = 7 * ONE_MONTH

    with open(ifname) as fobj:
        with open(deadname,'w') as dout, open(alivename,'w') as aout:
            for line in fobj:
                line = json.loads(line)

                startt = arrow.get(line[1]).timestamp
                endt = arrow.get(line[2]).timestamp

                # last post happened atleast before six months from end of dataset
                # and first post happened atleast 7 months before end of dataset
                if endtime - endt > SIX_MONTHS and endtime - startt > SEVEN_MONTHS:
                    dout.write(line[0] + " " + arrow.get(endt).isoformat() + "\n")

                # last post happened within one month from end of data set
                # and first post happened atleast 7 months before end of dataset
                if endtime - endt < ONE_MONTH and endtime - startt > SEVEN_MONTHS:
                    aout.write(line[0] + " " + arrow.get(endt).isoformat() + "\n")

if __name__ == '__main__':
    main()




